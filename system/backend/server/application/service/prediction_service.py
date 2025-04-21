from sqlalchemy.exc import SQLAlchemyError
from application.util import (fetch_ml_models, fetch_preprocessing_models,
                              json_data_preprocessor, make_prediction)


class Prediction_Service:

    @classmethod
    def predict_results(cls, json_data):
        try:
            fetch_preprocessing_models()
            fetch_ml_models()
            preprocessed_data = json_data_preprocessor(json_data)
            return  make_prediction(preprocessed_data)   
        except SQLAlchemyError as ex:
            raise             
        except FileNotFoundError as ex:
            raise
        except ValueError as ex:
            raise ValueError(
                "System cannot make predictions for untrained values"
            )