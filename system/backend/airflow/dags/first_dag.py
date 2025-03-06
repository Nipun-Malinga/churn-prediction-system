from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.model_trainer import train_model

default_args = {
    'owner': 'churn-pred-server',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'Test_Dag_v5',
    default_args = default_args,
    start_date = datetime(2025, 3, 3),
    schedule_interval = '@daily'
) as dag:
    task = PythonOperator(
        task_id = 'First_test_task',
        python_callable=train_model
    )

    task