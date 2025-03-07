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
    def preprocess():
        X_train, X_test, y_train, y_test = preprocess_dataset()
        return {
            "X_train": X_train, 
            "X_test": X_test, 
            "y_train": y_train, 
            "y_test": y_test
        }
    
    @task(multiple_outputs=True)
    def train(X_train, y_train):
        model_list = train_model(X_train, y_train)
        return {
            "model_list": model_list
        }
    
    @task(multiple_outputs=True)
    def evaluate(model_list, x_test, y_test):
        return {
            "model_evaluation_list": evaluate_model(model_list, x_test, y_test)
        }

    @task
    def update(model_evaluation_list):
        update_database(model_evaluation_list)

    preprocessed_data = preprocess()
    trained_models = train(preprocessed_data["X_train"],preprocessed_data["y_train"])
    evaluate_models = evaluate(trained_models["model_list"], preprocessed_data["X_test"], preprocessed_data["y_test"])
    update(evaluate_models["model_evaluation_list"])

training_dag = model_trainer()