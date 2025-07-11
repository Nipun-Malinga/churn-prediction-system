from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from application.utils import (
    fetch_ml_models,
    fetch_preprocessing_models,
    json_data_preprocessor,
    make_prediction,
)
from werkzeug.exceptions import NotFound


class Prediction_Service:

    @classmethod
    def predict_results(cls, json_data):
        try:
            fetch_preprocessing_models()
            fetch_ml_models()
            preprocessed_data = json_data_preprocessor(json_data)
            return make_prediction(preprocessed_data)
        except SQLAlchemyError:
            raise
        except NoResultFound:
            raise
        except ValueError:
            raise
        except NotFound:
            raise
        except Exception:
            raise
