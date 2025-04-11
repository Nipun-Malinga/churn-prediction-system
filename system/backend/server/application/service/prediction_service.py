import joblib
from application.util import (fetch_ml_models, fetch_preprocessing_models,
                              json_data_preprocessor, make_prediction)


class Prediction_Service:

    @classmethod
    def predict_results(cls, json_data):
        fetch_preprocessing_models()
        fetch_ml_models()
        try:
            preprocessed_data = json_data_preprocessor(json_data)
            prediction = make_prediction(preprocessed_data)
        except FileNotFoundError as err:
            raise FileNotFoundError(f"File not found: {err}") from err
        return prediction