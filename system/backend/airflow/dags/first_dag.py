from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'churn-pred-server',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id = 'Test_Dag',
    default_args = default_args,
    start_date = datetime(2025, 2, 27),
    schedule_interval = '@hourly'
) as dag:
    task = BashOperator(
        task_id = 'First_test_task',
        bash_command = 'echo hello airflow'
    )

    task