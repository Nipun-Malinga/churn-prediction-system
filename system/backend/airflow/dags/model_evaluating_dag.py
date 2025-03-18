from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from datetime import datetime, timedelta

from scripts.utils import fetch_evaluation_data

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
            "fetched_evaluation_data": fetched_evaluation_data
        }
    
    evaluation_dataset = fetching_evaluation_data()

evaluating_dag = model_evaluator()