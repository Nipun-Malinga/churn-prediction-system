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
        Data_Transformer_Info.id,
        Data_Transformer_Info.version_name
    ).join(Data_Transformer_Info).order_by(
        desc(Data_Transformer_Info.updated_date)
    ).where(
        Data_Transformer_Info.is_downloaded == False
    ).limit(Data_Transformer.query.count()).all()
    
    
    for info in result:
        print(f"Info: {info}")
        download_blob(
            f"data_transformers/{info[2]}", 
            join(DATA_TRANSFORMER_PATH, f"{info[0]}.pkl")
        )
        transformer_info_result = Data_Transformer_Info.query.get(info[1])
        print(f"Info_result: {transformer_info_result}")
        transformer_info_result.is_downloaded = True
        db.session.commit()
        
    
def fetch_ml_models():
    None