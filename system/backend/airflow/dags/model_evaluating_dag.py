from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator, ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

from scripts.utils import fetch_evaluation_data, fetch_trained_models
from scripts.data_preprocessor import preprocess_evaluation_data
from scripts.model_evaluator import evaluate_model, compare_model_performance

default_args = {
    'owner': 'churn-pred_server',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

@dag(dag_id='Model_Evaluating_DAG', default_args=default_args, start_date=days_ago(1), schedule_interval="@daily")
def model_evaluator():
    @task(multiple_outputs=True)
    def fetching_evaluation_data():
        fetched_evaluation_data = fetch_evaluation_data()   
        return {
            "evaluation_data": fetched_evaluation_data
        }
    
    @task(multiple_outputs=True)
    def preprocessing_data(evaluation_dataset):
        X_test, Y_test = preprocess_evaluation_data(evaluation_dataset)
        return {
            "X_test": X_test,
            "Y_test": Y_test
        }
        
    @task(multiple_outputs=True)
    def fetching_trained_models():
        trained_models = fetch_trained_models()
        return {
            "model_list": trained_models
        }
        
    @task(multiple_outputs=True)
    def evaluating_model_performance(model_list, x_test, y_test):
        model_evaluation_list = evaluate_model(model_list, x_test, y_test)
        return {
            "model_evaluation_list": model_evaluation_list
        }
        
    @task
    def comparing_model_performance(base_performance, evaluated_performance):
        accuracy_loss, retrain_model = compare_model_performance(base_performance, evaluated_performance)
        return {
            "accuracy_loss": accuracy_loss,
            "retrain_model": retrain_model
        }
   
    def check_evaluation_data(evaluation_data):
        if evaluation_data.empty or evaluation_data.shape[0] < 1000:  
            print("Evaluation data is empty. Stopping DAG.")
            return False
        return True
    
    def check_trained_models(trained_models):
        if not trained_models:
            return "trigger_retraining_dag"
        return "preprocessing_data"
           
    dataset = fetching_evaluation_data()
    trained_models = fetching_trained_models()

    short_circuit = ShortCircuitOperator(
        task_id="stop_if_no_evaluation_data",
        python_callable=check_evaluation_data,
        op_kwargs={"evaluation_data": dataset["evaluation_data"]},
    )
    
    branch_task = BranchPythonOperator(
        task_id="check_trained_models",
        python_callable=check_trained_models,
        op_kwargs={"trained_models": trained_models["model_list"]},
    )

    trigger_retraining_dag = TriggerDagRunOperator(
        task_id="trigger_retraining_dag",
        trigger_dag_id="Model_Training_DAG",
        wait_for_completion=True
    )

    preprocessed_data = preprocessing_data(dataset["evaluation_data"])

    evaluated_data = evaluating_model_performance(
        trained_models["model_list"], 
        preprocessed_data["X_test"], 
        preprocessed_data["Y_test"]
    )
    
    compared_data = comparing_model_performance(
        trained_models["model_list"],
        evaluated_data["model_evaluation_list"]
    )

    dataset >> short_circuit >> branch_task
    trained_models >> branch_task

    branch_task >> trigger_retraining_dag
    branch_task >> preprocessed_data >> evaluated_data >> compared_data
    
evaluating_dag = model_evaluator()