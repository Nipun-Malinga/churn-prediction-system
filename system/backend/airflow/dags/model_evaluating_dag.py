from datetime import timedelta
from typing import Dict, Union

import numpy as np
import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator, ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from scripts.data_preprocessor import preprocess_evaluation_data
from scripts.model_evaluator import (compare_model_performance, evaluate_model,
                                     update_accuracy_drift)
from scripts.utils import fetch_evaluation_data, fetch_trained_model_data

default_args = {
    'owner': 'churn-pred_server',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

@dag(dag_id='Model_Evaluating_DAG', default_args=default_args, start_date=days_ago(1), schedule_interval="@weekly")
def model_evaluator():
    
    @task(multiple_outputs=True)
    def fetching_evaluation_data() -> Dict[str, pd.DataFrame]:
        fetched_evaluation_data = fetch_evaluation_data()   
        return {
            "evaluation_data": fetched_evaluation_data
        }
    
    @task(multiple_outputs=True)
    def preprocessing_data(evaluation_dataset: pd.DataFrame) -> Dict[str, Union[np.array, bool]]:
        try:
            X_test, Y_test = preprocess_evaluation_data(evaluation_dataset)
            return {
                "X_test": X_test,
                "Y_test": Y_test,
                "retrain_model": False
            }
        except ValueError as exp:
            print("Untrained Value Detected. Triggering retraining.")
            return {
                "X_test": [],
                "Y_test": [],
                "retrain_model": True
            }

        
    @task(multiple_outputs=True)
    def fetching_trained_models() -> Dict[str, list]:
        trained_models = fetch_trained_model_data()
        return {
            "model_list": trained_models
        }
        
    @task(multiple_outputs=True)
    def evaluating_model_performance(model_list: list, x_test: np.array, y_test: np.array) -> Dict[str, list]:
        model_evaluation_list = evaluate_model(model_list, x_test, y_test)
        return {
            "model_evaluation_list": model_evaluation_list
        }
        
    @task(multiple_outputs=True)
    def comparing_model_performance(base_performance: list, evaluated_performance: list) -> Dict[str, Union[float, bool]]:
        accuracy_loss, retrain_model = compare_model_performance(base_performance, evaluated_performance)
        return {
            "accuracy_loss": accuracy_loss,
            "retrain_model": retrain_model
        }
        
    @task
    def update_model_info(model_info: list, evaluation_data: list, accuracy_drift: float) -> None:
        update_accuracy_drift(model_info, evaluation_data, accuracy_drift)
     
    """ Task Calls """  
    
    fetched_data = fetching_evaluation_data()
    
    trained_models = fetching_trained_models()
   
    preprocessed_data = preprocessing_data(fetched_data["evaluation_data"])
    
    evaluated_data = evaluating_model_performance(
        trained_models["model_list"], 
        preprocessed_data["X_test"], 
        preprocessed_data["Y_test"]
    )
    
    compared_data = comparing_model_performance(
        trained_models["model_list"],
        evaluated_data["model_evaluation_list"]
    )
    
    """ Conditional Switch """    
   
    def check_evaluation_data(evaluation_data: pd.DataFrame) -> bool:
        if evaluation_data is None or evaluation_data.empty or evaluation_data.shape[0] < 1000:  
            print("Evaluation data is empty. Stopping DAG.")
            return False
        return True
    
    def check_trained_models(trained_models: list) -> str:
        if not trained_models:
            return "trigger_retraining_dag"
        return "preprocessing_data"
    
    def check_untrained_data(retrain_model: bool) -> str:
        if retrain_model:
            return "trigger_retraining_dag_02"
        return "evaluating_model_performance"
    
    def decide_approach(retrain_model: bool) -> str:
        if retrain_model:
            return "trigger_retraining_dag_01"
    
    """Conditional Tasks"""
    
    short_circuit = ShortCircuitOperator(
        task_id="stop_if_no_evaluation_data",
        python_callable=check_evaluation_data,
        op_kwargs={"evaluation_data": fetched_data["evaluation_data"]},
    )
    
    trigger_retraining_dag_01 = TriggerDagRunOperator(
        task_id="trigger_retraining_dag_01",
        trigger_dag_id="Model_Training_DAG",
        wait_for_completion=True
    )
    
    trigger_retraining_dag_02 = TriggerDagRunOperator(
        task_id="trigger_retraining_dag_02",
        trigger_dag_id="Model_Training_DAG",
        wait_for_completion=True
    )
    
    branch_task_01 = BranchPythonOperator(
        task_id="stop_if_no_trained_models",
        python_callable=check_trained_models,
        op_kwargs={"trained_models": trained_models["model_list"]},
    )
    
    branch_task_02 = BranchPythonOperator(
        task_id="check_for_untrained_data",
        python_callable=check_untrained_data,
        op_kwargs={"retrain_model": preprocessed_data["retrain_model"]}
    )
    
    branch_task_03 = BranchPythonOperator(
        task_id="deciding_approach",
        python_callable=decide_approach,
        op_kwargs={"retrain_model": compared_data["retrain_model"]}
    )
    
    """ Dependencies """
    
    fetched_data >> short_circuit >> branch_task_01
    
    trained_models >> branch_task_01

    branch_task_01 >> [trigger_retraining_dag_01, preprocessed_data]
    
    preprocessed_data >> branch_task_02
    
    branch_task_02 >> [trigger_retraining_dag_02, evaluated_data]
    
    compared_data >> update_model_info(
        trained_models["model_list"],
        evaluated_data["model_evaluation_list"], 
        compared_data["accuracy_loss"]
    )
    
    compared_data >> branch_task_03 >> trigger_retraining_dag_01
    
evaluating_dag = model_evaluator()