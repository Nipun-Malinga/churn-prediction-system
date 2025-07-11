import os

from google.cloud import storage
from google.cloud.exceptions import NotFound as GCSNotFound
from werkzeug.exceptions import NotFound
from flask import current_app

storage_client = storage.Client()
bucket_name = "churn_prediction_model_storage"


def download_blob(source_blob_path, destination_file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_path)

        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)

        blob.download_to_filename(destination_file_name)
        current_app.logger.info(
            f"Downloaded {destination_file_name} to {source_blob_path}"
        )

    except GCSNotFound as ex:
        raise NotFound(
            f"File: {destination_file_name} not found in cloud storage"
        ) from ex
    except Exception as ex:
        current_app.logger.error(f"Failed to Download {source_blob_path}")
