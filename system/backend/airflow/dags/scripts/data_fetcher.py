import pandas as pd

from sqlalchemy import text
from scripts import database_engine

def fetch_training_data():
    with database_engine().connect() as conn:
        dataset = pd.read_sql(
            sql="SELECT * FROM evaluation_data",
            con=conn.connection
        )
        return dataset


def fetch_evaluation_data() -> pd.DataFrame:
    with database_engine().connect() as conn:
        try:
            fetched_last_updated_date = conn.execute(
                text("SELECT updated_date FROM model_info ORDER BY updated_date DESC LIMIT 1")
            ).scalar() 

            if fetched_last_updated_date is None:
                print("No updated_date found in model_info.")
                return None
            
            evaluation_dataset = pd.read_sql(
                sql=f"SELECT * FROM evaluation_data WHERE added_date > {fetched_last_updated_date}",
                con=conn.connection
            )
            
            return evaluation_dataset
        except Exception as ex:
            print(f"Error fetching evaluation data: {ex}")
