from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta

from scripts.utils import fetch_evaluation_data, fetch_trained_models
from scripts.data_preprocessor import preprocess_evaluation_data
from scripts.model_evaluator import evaluate_model

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
        
        if fetched_evaluation_data.empty:
            raise AirflowFailException("No data in database. Programme terminated.")
        
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
    
    dataset = fetching_evaluation_data()
    preprocessed_data = preprocessing_data(dataset["evaluation_data"])
    trained_models = fetching_trained_models()
    evaluated_data = evaluating_model_performance(trained_models["model_list"], preprocessed_data["X_test"], preprocessed_data["Y_test"])
    
evaluating_dag = model_evaluator()