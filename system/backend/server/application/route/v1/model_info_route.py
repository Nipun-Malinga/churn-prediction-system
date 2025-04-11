from enum import Enum, auto

from flask import Blueprint, request, jsonify
from application.service import Model_Info_Service
from application.response import response_template, error_response_template
from sqlalchemy.exc import NoResultFound

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
    
@model.route("/", methods=["GET"])
def get_all_models():
    
    try:
        return response_template(
            "success",
            "Models Fetched Successfully",
            service.get_all_models()
        ), 200
    except Exception as ex:
        return error_response_template("Failed to Fetch Models"), 500
    
@model.route("/info/basic", methods=["GET"])    
def get_basic_model_info_by_id():
    
    model_id = request.args.get("model_id") 
    try:
        return response_template(
            "success",
            "Model Information Fetched Successfully",
            service.get_basic_model_info(request.args.get("model_id"))
        ), 200
    except NoResultFound as ex:
        return error_response_template(f"No model info found for model_id: {model_id}"), 404
    except Exception as ex:
        return error_response_template("Failed to fetch Model Information"), 500
    
@model.route("/info/advanced", methods=["GET"])    
def get_advanced_model_info_by_id():
    
    model_id = request.args.get("model_id")
    try:
        return response_template(
            "success",
            "Model Information Fetched Successfully",
            service.get_advanced_model_info(model_id)
        ), 200
    except NoResultFound as ex:
        return error_response_template(f"No model info found for model_id: {model_id}"), 404
    except Exception as ex:
        return error_response_template("Failed to fetch Model Information"), 500

@model.route("/charts", methods=["GET"])   
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
        
    except Exception as ex:
        return error_response_template("Failed to fetch chart history"), 500