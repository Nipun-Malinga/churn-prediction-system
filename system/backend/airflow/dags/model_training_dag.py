from airflow.decorators import dag, task
from datetime import datetime, timedelta
from scripts.model_trainer import preprocess_dataset, train_model, update_database
from scripts.model_evaluator import evaluate_model

default_args = {
    'owner': 'churn-pred-server',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

@dag(dag_id='Model_Training_DAG', default_args=default_args, start_date=datetime(2025, 3, 6), schedule_interval="@daily")
def model_trainer():
    @task(multiple_outputs=True)
    def data_preprocess():
        X_train, X_test, y_train, y_test = preprocess_dataset()
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
    def database_update(model_evaluation_list):
        update_database(model_evaluation_list)

    preprocessed_data = data_preprocess()
    trained_models = model_training(preprocessed_data["X_train"],preprocessed_data["y_train"])
    evaluate_models = model_evaluation(trained_models["model_list"], preprocessed_data["X_test"], preprocessed_data["y_test"])
    database_update(evaluate_models["model_evaluation_list"])

training_dag = model_trainer()