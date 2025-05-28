import os

from google.cloud import storage
from flask import current_app

storage_client = storage.Client()
bucket_name = "churn_prediction_model_storage"

def download_blob(source_blob_path, destination_file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_path)

        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)

        blob.download_to_filename(destination_file_name)
        current_app.logger.info("Downloaded %s to %s", destination_file_name, source_blob_path)
    
    except Exception as ex:
        current_app.logger.error("Error: Failed to Download %s.  %s", source_blob_path, ex)
        