from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from application.service import  predict_results
from application.schema import Prediction_Request_Schema

predict_result = Blueprint('predict_bp', __name__)

@predict_result.route('/predict', methods=['POST'])
def predict():
    schema = Prediction_Request_Schema()
    try:
        request_data = schema.load(request.json)
        return jsonify({"prediction": predict_results(request_data)[0]}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400