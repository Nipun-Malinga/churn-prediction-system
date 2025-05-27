from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Prediction_Request_Schema
from application.services import Prediction_Service
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

predict_result = Blueprint("predict_bp", __name__)

service = Prediction_Service()

@predict_result.route("/predict", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
def predict():
    schema = Prediction_Request_Schema()
     
    try:
        request_data = schema.load(request.json)
        prediction, probability = service.predict_results(request_data)
        
        current_app.logger.info("Churn Predicted Successfully")

        return response_template(
            "success", 
            "Model prediction success", 
            {
                "Prediction": prediction[0], 
                "Probability": probability
            }
        ), 200
        
    except ValidationError as ex:
        current_app.logger.error("Validation Error: %s", ex, exc_info=True)
        return error_response_template(ex.messages), 400 
    except FileNotFoundError as ex:
        current_app.logger.error("Service Unavailable Error: %s", ex, exc_info=True)
        return error_response_template("Error: Service Unavailable"), 503 
    except ValueError as ex:
        current_app.logger.error("Value Error: %s", ex, exc_info=True)
        return error_response_template("Error: Invalid Prediction Value Detected"), 400 
    except SQLAlchemyError as ex:
        current_app.logger.error("Database Error: %s", ex, exc_info=True)
        return error_response_template("Error: Database Error Occurred"), 500
    except Exception as ex:
        current_app.logger.error("Unexpected Error: %s", ex, exc_info=True)
        return error_response_template("Error: Server Error Occurred"), 500