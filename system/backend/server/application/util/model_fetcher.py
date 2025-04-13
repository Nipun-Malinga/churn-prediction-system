from os.path import abspath, dirname, join

from application import db
from application.model.data_transformer import Data_Transformer
from application.model.data_transformer_info import Data_Transformer_Info
from application.model.model import Model
from application.model.model_info import Model_Info
from application.util.cloud_storage_utils import download_blob
from sqlalchemy import desc

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

DATA_TRANSFORMER_PATH = join(BASE_DIR, "data_transformers/")
ML_MODEL_PATH = join(BASE_DIR, "ml_models/")

def fetch_preprocessing_models():
    try:
        result = db.session.query(
            Data_Transformer.name, 
            Data_Transformer_Info.id,
            Data_Transformer_Info.version_name
        ).join(
            Data_Transformer_Info
        ).order_by(
            desc(Data_Transformer_Info.updated_date)
        ).where(
            Data_Transformer_Info.is_downloaded == False
        ).limit(
            Data_Transformer.query.count()
        ).all()

        for info in result:
            name, id, version_name = info

            try:
                download_blob(
                    f"data_transformers/{version_name}", 
                    join(DATA_TRANSFORMER_PATH, f"{name}.pkl")
                )
                transformer_info_result = Data_Transformer_Info.query.get(id)
                transformer_info_result.is_downloaded = True
            except Exception as ex:
                db.session.rollback()
                continue
        db.session.commit() 
    except Exception as ex:
        db.session.rollback()
    finally:
        db.session.close()
        
    
def fetch_ml_models():
    try:
        result = db.session.query(
            Model.name,
            Model_Info.id,
            Model_Info.version_name
        ).join(
            Model_Info
        ).order_by(
            desc(Model_Info.updated_date)
        ).where(
            Model_Info.is_downloaded == False,  
            Model.base_model == True
        ).limit(1)

        name, id, version_name = result.first()

        try:
            download_blob(
                f"ml_models/{version_name}",
                join(ML_MODEL_PATH, f"{name}.pkl")
            )

            model_info_result = Model_Info.query.get(id)
            model_info_result.is_downloaded = True
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            
    except Exception as ex:
        db.session.rollback()
    finally:
        db.session.close()
