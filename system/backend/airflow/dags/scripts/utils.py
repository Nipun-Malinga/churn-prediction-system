import os
import pandas as pd
import joblib
from datetime import datetime

from sqlalchemy import text, exc
from scripts import database_engine
from google.cloud import storage

from os.path import join, dirname, abspath

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
                sql=f"SELECT * FROM evaluation_data WHERE added_date > '{fetched_last_updated_date}'",
                con=conn.connection
            )
            
            return evaluation_dataset
        except Exception as ex:
            print(f"Error fetching evaluation data: {ex}")

def fetch_trained_models():
    ABS_DIR = dirname(abspath(__file__))
    BASE_DIR = join(ABS_DIR, "trained_models/")

    ML_MODEL_PATHS = {
        "versioned": join(BASE_DIR, "ml_models/versioned/"),
    }
    
    with database_engine().connect() as connection:
        model_data = []
        
        model_data_result = connection.execute(text(
            """
                SELECT name, accuracy, f1_score, version_name 
                FROM model_info 
                INNER JOIN model ON model_info.model_id = model.id
                WHERE base_model IS TRUE
                ORDER BY updated_date 
                DESC 
                LIMIT (SELECT COUNT(*) FROM model)
            """
        )).fetchall()
          
        for data in model_data_result:
            model_data.append({
                    "model": joblib.load(join(ML_MODEL_PATHS["versioned"], data[3])),
                    "name": data[0],
                    "version": data[3],
                    "base_model": None
            })
    
    return model_data
                 
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
            except exc.SQLAlchemyError as ex:
                print(f"Error updating database: {ex}")
            
            try:
                os.remove(join(path, version_name_result[0]))
            except FileNotFoundError as ex:
                print(f"Failed to delete model. File not found: {version_name_result[0]}")

def update_database(model_info_list, data_transformer_list):

    with database_engine().connect() as connection:
        try:
            for model_info in model_info_list:
                model_id_result = connection.execute(
                    text("SELECT id FROM model WHERE name = :model_name"), {"model_name": model_info["model_name"]}
                ).fetchone()

                if not model_id_result:
                    model_id_result = connection.execute(
                        text("INSERT INTO model (name, base_model) VALUES (:name, :base_model) RETURNING id"), {"name": model_info["model_name"], "base_model": model_info["base_model"]}
                    ).fetchone()

                model_id = model_id_result[0] 

                model_info_query = text("""
                    INSERT INTO model_info 
                    (model_id, updated_date, accuracy, "TP", "TN", "FP", "FN", precision, recall, f1_score, is_automated_tunning, version_name)
                    VALUES 
                    (:model_id, :updated_date, :accuracy, :TP, :TN, :FP, :FN, :precision, :recall, :f1_score, :is_automated_tunning, :version_name)
                """)

                connection.execute(model_info_query, {
                    "model_id": model_id,
                    "updated_date": datetime.now(),
                    "accuracy": float(model_info["accuracy"]), 
                    "TP": int(model_info["tp"]),
                    "TN": int(model_info["tn"]),
                    "FP": int(model_info["fp"]),
                    "FN": int(model_info["fn"]),
                    "precision": float(model_info["precision"]),
                    "recall": float(model_info["recall"]),
                    "f1_score": float(model_info["f1_score"]),
                    "is_automated_tunning": True,
                    "version_name": model_info["version_name"]
                })

                print("Machine Learning Model Related Data Updated Successfully!")

        except Exception as ex:
            print(f"Error adding model info to the database: {ex}")
            
        try:
            for data_transformer in data_transformer_list:
                data_transformer_id_result = connection.execute(
                    text("SELECT id FROM data_transformer WHERE name = :name"), 
                    {
                        "name": data_transformer["transformer_name"]
                    }
                ).fetchone()
                
                if not data_transformer_id_result:
                    data_transformer_id_result = connection.execute(
                        text("INSERT INTO data_transformer (name) VALUES (:name) RETURNING id"),
                        {
                            "name": data_transformer["transformer_name"]
                        }
                    ).fetchone()
                    
                data_transformer_id = data_transformer_id_result[0]
          
                connection.execute(
                    text(
                        """
                        INSERT INTO data_transformer_info (data_transformer_id, updated_date, version_name) 
                        VALUES (:data_transformer_id, :updated_date, :version_name)
                        """
                    ),
                    {
                        "data_transformer_id": data_transformer_id,
                        "updated_date": datetime.now(),
                        "version_name": data_transformer["version"],
                    }
                )
                
                print("Data Transformers Related Data Updated Successfully!")
                    
        except Exception as ex:
            print(f"Error adding data_transformer info to the database: {ex}")