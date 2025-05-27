from enum import Enum

from marshmallow import ValidationError

from application import limiter
from application.responses import error_response_template, response_template
from application.services import Model_Info_Service
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from application.schemas import Evaluation_Threshold_Schema

model = Blueprint("model_bp", __name__)

service = Model_Info_Service()

"""
 Add a method to convert all data to dict in models.
""" 
class Type(Enum):
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    

@model.route("", methods=["GET"])    
@limiter.limit("10 per minute")
@jwt_required()
def get_models():
    try:
        return response_template(
            "success",
            "Models Fetched Successfully",
            service.get_all_models()
        ), 200
        
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Server Error: Failed to Fetch Models"
        ), 500


@model.route("/info", methods=["GET"])    
@limiter.limit("10 per minute")
@jwt_required()
def get_basic_model():
    try:
        return response_template(
            "success",
            "Model Information Fetched Successfully",
            service.get_basic_model_info()
        ), 200
        
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to fetch Model Information"
        ), 500


    
@model.route("/info/advanced", methods=["GET"])   
@limiter.limit("10 per minute")
@jwt_required() 
def get_advanced_model_info_by_id():
    
    model_id = request.args.get("model_id")
    try:
        return response_template(
            "success",
            "Model Information Fetched Successfully",
            service.get_advanced_model_info(model_id)
        ), 200
        
    except NoResultFound as ex:
        return error_response_template(
            f"No model info found for model_id: {model_id}"
        ), 404
    except SQLAlchemyError as ex: 
        return error_response_template(
            f"Database error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to fetch Model Information"
        ), 500


    
@model.route("/base", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required() 
def get_base_model_performance(): 
    try:
        return response_template(
            "success", 
            "Base Model Data Successfully", 
            service.get_base_model_performance()
        ), 200
    
    except SQLAlchemyError as ex: 
        return error_response_template(
            f"Database error: {str(ex)}"
        ), 500    
    except Exception as ex:
        return error_response_template(
            "Failed to fetch model information"
        ), 500



@model.route("/charts", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required() 
def model_history_chart_data():
    try:
        model_id = request.args.get("model_id")
        filter_by = request.args.get("filter_type")

        if not model_id:
            return error_response_template("Missing required parameters"), 400

        Type(filter_by)
        
        return response_template(
            "success",
            f"{filter_by.capitalize()} Data Fetched Successfully",
            service.model_performance_history(model_id, filter_by)
        )
    
    except ValueError as ex:
        return error_response_template(
            f"Invalid Filtering Value",
        ), 400
    except SQLAlchemyError as ex: 
        return error_response_template(
            f"Database error: {str(ex)}"
        ), 500    
    except Exception as ex:
        return error_response_template(
            "Failed to fetch chart history"
        ), 500
    

    
@model.route("/drift", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required() 
def get_model_performance_drift(): 
    try:
        return response_template(
            "success", 
            "Drift History Fetched Successfully", 
            service.model_drift_history()
        ), 200
    except SQLAlchemyError as ex: 
        return error_response_template(
            f"Database error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to fetch drift history"
        ), 500


        
@model.route("/production", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()        
def get_new_trained_models():
    try:
        return response_template(
            "success",
            "New Trained Models Fetched Successfully",
            service.new_trained_models()
        ), 200
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to fetch new trained models"
        ), 500
        
@model.route("/production", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()        
def set_production_model():
    
    # batch_id = request.args.get("batch_id")
        
    # if not batch_id:
    #     return error_response_template(
    #         "Missing required parameters"
    #     ), 400
        
    # return response_template(
    #         "success",
    #         "Production Models Set Successfully",
    #         service.production_model(batch_id)
    #     )   
    
    try:
        batch_id = request.args.get("batch_id")
        
        if not batch_id:
            return error_response_template(
                "Missing required parameters"
            ), 400
        
        return response_template(
            "success",
            "Production Models Set Successfully",
            service.production_model(batch_id)
        )    
        
    except NoResultFound as ex:
        return error_response_template(
            f"{str(ex)}"
        ), 404
    except Exception as ex:
        return error_response_template(
            "Failed to set production model"
        ), 500
        
@model.route("/evaluation-threshold", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()        
def set_evaluation_threshold():
    schema = Evaluation_Threshold_Schema()
    try:
        request_data = schema.load(request.json)
        return response_template(
            "success", 
            "Evaluation thresholds set successfully", 
            schema.dump(service.set_threshold(request_data))
        ), 201
        
    except ValidationError as err:
        return error_response_template(
            err.messages
        ), 400
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to set evaluation threshold"
        ), 500
        
@model.route("/evaluation-threshold", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()        
def get_evaluation_threshold():
    try:
        return response_template(
            "success", 
            "Evaluation thresholds fetched successfully", 
            service.get_threshold()
        ), 201

    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            "Failed to set evaluation threshold"
        ), 500
    