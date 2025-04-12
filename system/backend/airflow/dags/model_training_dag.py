from datetime import timedelta
from typing import Dict, Union

import numpy as np
import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.python import ShortCircuitOperator
from airflow.utils.dates import days_ago
from scripts.data_preprocessor import (deploy_preprocessing_models,
                                       preprocess_dataset)
from scripts.model_evaluator import evaluate_model
from scripts.model_trainer import deploy_models, train_model
from scripts.utils import fetch_training_data, update_model_info

default_args = {
    'owner': 'churn-pred-server',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

@dag(dag_id='Model_Training_DAG', default_args=default_args, start_date=days_ago(1), schedule_interval="@once")
def model_trainer():
    @task(multiple_outputs=True)
    def fetching_training_data() -> Dict[str, pd.DataFrame]:
        fetched_data = fetch_training_data()  
        return {
            "fetched_data": fetched_data
        }

    @task(multiple_outputs=True)
    def preprocessing_data(dataset: pd.DataFrame) -> Dict[str, Union[np.array, list]]:
        X_train, X_test, y_train, y_test, data_transformer_list = preprocess_dataset(dataset)
        return {
            "X_train": X_train, 
            "X_test": X_test, 
            "y_train": y_train, 
            "y_test": y_test,
            "data_transformer_list": data_transformer_list
        }
    
    @task
    def deploying_processing_models(data_transformer_list: list) -> None:
        deploy_preprocessing_models(data_transformer_list)
    
    @task(multiple_outputs=True)
    def training_ml_model(X_train: np.array, y_train: np.array) -> Dict[str, list]:
        model_list = train_model(X_train, y_train)
        return {
            "model_list": model_list
        }
    
    @task(multiple_outputs=True)
    def evaluating_model_performance(model_list: list, x_test: np.array, y_test: np.array) -> Dict[str, list]:
        model_evaluation_list = evaluate_model(model_list, x_test, y_test)
        return {
            "model_evaluation_list": model_evaluation_list
        }

    @task
    def updating_database(model_evaluation_list: list, data_transformer_list: list) -> None:
        update_model_info(model_evaluation_list, data_transformer_list)

    @task
    def deploying_ml_models(model_list: list) -> None:
        deploy_models(model_list)
    
    """ Task Calls """

    training_data = fetching_training_data()
    
    preprocessed_data = preprocessing_data(training_data["fetched_data"])
    
    trained_models = training_ml_model(
        preprocessed_data["X_train"], 
        preprocessed_data["y_train"]
    )
    
    evaluation_data = evaluating_model_performance(
        trained_models["model_list"], 
        preprocessed_data["X_test"], 
        preprocessed_data["y_test"]
    )
    
    """ Conditional Switch """ 
    
    def check_training_data(fetched_data: pd.DataFrame) -> bool:
        if fetched_data.empty:
            return False
        return True
    
    """Conditional Tasks"""
    
    short_circuit = ShortCircuitOperator(
        task_id="stop_if_no_training_data",
        python_callable=check_training_data,
        op_kwargs={"fetched_data": training_data["fetched_data"]},
    )
    
    """ Dependencies """

    training_data >> short_circuit >> preprocessed_data
    
    preprocessed_data >> deploying_processing_models(preprocessed_data["data_transformer_list"])
    
    preprocessed_data >> trained_models
    
    trained_models >> evaluation_data
    
    evaluation_data >> updating_database(
        evaluation_data["model_evaluation_list"], 
        preprocessed_data["data_transformer_list"]
    )
    
    trained_models >> deploying_ml_models(trained_models["model_list"])

training_dag = model_trainer()