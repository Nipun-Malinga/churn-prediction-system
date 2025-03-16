import os
import pandas as pd

from sqlalchemy import text
from scripts import database_engine
from google.cloud import storage

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

def upload_to_gcs(bucket_name, source_file_path, destination):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination)

    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to {destination} in {bucket_name}.")

def remove_models(path, query):
        with database_engine().connect() as conn:
            try:
                version_name_result = conn.execute(text(query)).fetchone()

                os.remove(path, version_name_result[0])

            except Exception as ex:
                print(f"Error updating database: {ex}")
