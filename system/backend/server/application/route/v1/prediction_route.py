from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from application import limiter
from application.service import  predict_results
from application.schema import Prediction_Request_Schema
from application.response import response_template, error_response_template

predict_result = Blueprint("predict_bp", __name__)

@predict_result.route("/predict", methods=["POST"])
@limiter.limit("5 per minute")
def predict():
    schema = Prediction_Request_Schema()
    try:
        request_data = schema.load(request.json)
        
        prediction, probability = predict_results(request_data)

        return response_template("success", "Model prediction success", {"Prediction": prediction[0], "Probability": probability}), 200
    except ValidationError as err:
        return error_response_template(err.messages), 400
    except FileNotFoundError as err:
        return error_response_template(
            "Sorry there ara no trained models currently available."
        ), 503