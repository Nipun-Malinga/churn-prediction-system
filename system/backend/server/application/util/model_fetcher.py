from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from os.path import join, dirname, abspath
from application import db
from application.util.cloud_storage_utils import download_blob
from application.model.data_transformer import Data_Transformer
from application.model.data_transformer_info import Data_Transformer_Info
from application.model.model import Model
from application.model.model_info import Model_Info

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
        download_blob(
            f"data_transformers/{info[2]}", 
            join(DATA_TRANSFORMER_PATH, f"{info[0]}.pkl")
        )
        transformer_info_result = Data_Transformer_Info.query.get(info[1])
        transformer_info_result.is_downloaded = True
        db.session.commit()
        
    db.session.close()
        
    
def fetch_ml_models():
    result = db.session.query(
        Model.name,
        Model_Info.id,
        Model_Info.version_name
    ).join(Model_Info).order_by(
        desc(Model_Info.updated_date)
    ).where(
        Model_Info.is_downloaded == False,  Model.base_model == True
    ).limit(1).all()
    
    for model in result:
        download_blob(
            f"ml_models/{model[2]}",
            join(ML_MODEL_PATH, f"{model[0]}.pkl")
        )
        
        model_info_result = Model_Info.query.get(model[1])
        model_info_result.is_downloaded = True
        db.session.commit()
        
    db.session.close()