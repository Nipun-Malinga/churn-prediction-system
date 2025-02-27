import joblib
from application.util import json_data_preprocessor, make_prediction

def predict_results(json_data):
    preprocessed_data = json_data_preprocessor(json_data)
    prediction = make_prediction(preprocessed_data)
    return prediction