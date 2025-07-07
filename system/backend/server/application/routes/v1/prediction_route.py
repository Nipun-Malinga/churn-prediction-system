from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Prediction_Request_Schema
from application.services import Prediction_Service
from application.wrappers import apiWrapper
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

predict_result = Blueprint("predict_bp", __name__)

service = Prediction_Service()


@predict_result.route("/predict", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def predict():
    schema = Prediction_Request_Schema()

    request_data = schema.load(request.json)
    prediction, probability = service.predict_results(request_data)

    current_app.logger.info("Churn Predicted Successfully")
    return (
        response_template(
            "success",
            "Model prediction success",
            {"Prediction": prediction[0], "Probability": probability},
        ),
        200,
    )
