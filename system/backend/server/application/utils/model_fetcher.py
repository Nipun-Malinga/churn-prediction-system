from os.path import abspath, dirname, join

from flask import current_app
from application import db
from application.models.data_transformer import Data_Transformer
from application.models.data_transformer_info import Data_Transformer_Info
from application.models.model import Model
from application.models.model_info import Model_Info
from application.utils.cloud_storage_utils import download_blob
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

DATA_TRANSFORMER_PATH = join(BASE_DIR, "data_transformers/")
ML_MODEL_PATH = join(BASE_DIR, "ml_models/")


def fetch_preprocessing_models():
    try:
        result = (
            db.session.query(
                Data_Transformer.name,
                Data_Transformer_Info.id,
                Data_Transformer_Info.version_name,
            )
            .join(Data_Transformer_Info)
            .order_by(desc(Data_Transformer_Info.updated_date))
            .where(Data_Transformer_Info.is_downloaded == False)
            .limit(Data_Transformer.query.count())
            .all()
        )

        for info in result:
            name, id, version_name = info

            try:
                download_blob(
                    f"data_transformers/{version_name}",
                    join(DATA_TRANSFORMER_PATH, f"{name}.pkl"),
                )
                transformer_info_result = Data_Transformer_Info.query.get(id)
                transformer_info_result.is_downloaded = True
            except NotFound:
                current_app.logger.warning(f"File Not Found: {version_name}")
                raise
            except Exception:
                current_app.logger.error(
                    f"Failed to download or update transformer {name}: {ex}",
                    exc_info=True,
                )
                raise

        db.session.commit()

    except SQLAlchemyError as ex:
        current_app.logger.error(
            current_app.logger.error(
                f"Database Error: During fetch_preprocessing_models: {ex}",
                exc_info=True,
            )
        )
        db.session.rollback()
        raise
    except Exception as ex:
        current_app.logger.error(
            f"Unexpected error in fetch_preprocessing_models: {ex}", exc_info=True
        )
        db.session.rollback()
    finally:
        db.session.close()


def fetch_ml_models():
    try:
        result = (
            db.session.query(Model.name, Model_Info.id, Model_Info.version_name)
            .join(Model_Info)
            .order_by(desc(Model_Info.updated_date))
            .where(
                Model_Info.is_downloaded == False,
                Model_Info.is_production_model == True,
                Model.base_model == True,
            )
            .limit(1)
        )

        name, id, version_name = result.first()

        try:
            download_blob(
                f"ml_models/{version_name}", join(ML_MODEL_PATH, f"{name}.pkl")
            )

            model_info_result = Model_Info.query.get(id)
            model_info_result.is_downloaded = True
            db.session.commit()
        except NotFound as ex:
            current_app.logger.warning(f"File Not Found: {version_name}")
        except Exception as ex:
            current_app.logger.error(
                f"Failed to Download or Update ML Model: {name}: {ex}", exc_info=True
            )
            db.session.rollback()
            raise

    except SQLAlchemyError as ex:
        current_app.logger.error(
            current_app.logger.error(
                f"Database Error: During fetch_ml_models: {ex}",
                exc_info=True,
            )
        )
        db.session.rollback()
        raise
    except Exception as ex:
        current_app.logger.error(
            f"Unexpected error in fetch_ml_models: {ex}", exc_info=True
        )
        db.session.rollback()
        raise
    finally:
        db.session.close()
