from application import limiter
from application.response import error_response_template, response_template
from application.schema import Prediction_Request_Schema
from application.service import Prediction_Service
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

predict_result = Blueprint("predict_bp", __name__)

service = Prediction_Service()

@predict_result.route("/predict", methods=["POST"])
@limiter.limit("5 per minute")
@jwt_required()
def predict():
    schema = Prediction_Request_Schema()
    try:
        request_data = schema.load(request.json)
         
        prediction, probability = service.predict_results(request_data)

        return response_template(
            "success", 
            "Model prediction success", 
            {
                "Prediction": prediction[0], 
                "Probability": probability
            }
        ), 200
        
    except ValidationError as ex:
        return error_response_template(
            str(ex)
        ), 400
    except FileNotFoundError as ex:
        return error_response_template(
            str(ex)
        ), 503
    except ValueError as ex:
        return error_response_template (
            str(ex)
        ), 400
    except SQLAlchemyError as ex:
        return error_response_template (
            str(ex)
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to make prediction."
        ), 500