from sqlalchemy import create_engine
from airflow.hooks.base import BaseHook

def database_engine(): 
    try:
        conn = BaseHook.get_connection("CHURN_SERVER_DB")
        database_url = f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        return create_engine(database_url)
    except Exception as e:
        print(f"Error fetching Airflow connection: {e}")
