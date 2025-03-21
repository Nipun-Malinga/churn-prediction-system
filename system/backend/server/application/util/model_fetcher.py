from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from os.path import join, dirname, abspath
from application import db
from application.util.cloud_storage_utils import download_blob
from application.model.data_transformer import Data_Transformer
from application.model.data_transformer_info import Data_Transformer_Info

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

DATA_TRANSFORMER_PATH = join(BASE_DIR, "data_transformers/")
ML_MODEL_PATH = join(BASE_DIR, "ml_models/")

def fetch_preprocessing_models():
    result = db.session.query(
        Data_Transformer.name, 
        Data_Transformer_Info.version_name
    ).join(Data_Transformer_Info).order_by(
        desc(Data_Transformer_Info.updated_date)
    ).limit(Data_Transformer.query.count())
    
    for info in result:
        download_blob(
            f"data_transformers/{info[1]}", 
            join(DATA_TRANSFORMER_PATH, f"{info[0]}.pkl")
        ) 
    
def fetch_ml_models():
    None