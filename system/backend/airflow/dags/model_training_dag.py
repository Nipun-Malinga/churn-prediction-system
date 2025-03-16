from airflow.decorators import dag, task
from datetime import datetime, timedelta
from scripts.data_fetcher import fetch_training_data
from scripts.preprocess_data import preprocess_dataset
from scripts.model_trainer import train_model, update_database
from scripts.model_evaluator import evaluate_model

default_args = {
    'owner': 'churn-pred-server',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

@dag(dag_id='Model_Training_DAG', default_args=default_args, start_date=datetime(2025, 3, 14), schedule_interval="@daily")
def model_trainer():
    @task(multiple_outputs=True)
    def fetching_training_data():
        fetched_data = fetch_training_data()
        return {
            "fetched_data": fetched_data
        }

    @task(multiple_outputs=True)
    def preprocessing_data(dataset):
        X_train, X_test, y_train, y_test = preprocess_dataset(dataset)
        return {
            "X_train": X_train, 
            "X_test": X_test, 
            "y_train": y_train, 
            "y_test": y_test
        }
    
    @task(multiple_outputs=True)
    def model_training(X_train, y_train):
        model_list = train_model(X_train, y_train)
        return {
            "model_list": model_list
        }
    
    @task(multiple_outputs=True)
    def model_evaluation(model_list, x_test, y_test):
        model_evaluation_list = evaluate_model(model_list, x_test, y_test)
        return {
            "model_evaluation_list": model_evaluation_list
        }

    @task
    def updating_database(model_evaluation_list):
        update_database(model_evaluation_list)

    data = fetching_training_data()
    preprocessed_data = preprocessing_data(data["fetched_data"])
    trained_models = model_training(preprocessed_data["X_train"],preprocessed_data["y_train"])
    evaluate_models = model_evaluation(trained_models["model_list"], preprocessed_data["X_test"], preprocessed_data["y_test"])
    updating_database(evaluate_models["model_evaluation_list"])

training_dag = model_trainer()