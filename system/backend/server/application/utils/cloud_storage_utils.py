import os

from google.cloud import storage

storage_client = storage.Client()
bucket_name = "churn_prediction_model_storage"

def download_blob(source_blob_path, destination_file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_path)

        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)

        blob.download_to_filename(destination_file_name)
        print(f"Downloaded {source_blob_path} to {destination_file_name}")
    
    except Exception as ex:
        print(f"Error downloading {source_blob_path}: {ex}")
        