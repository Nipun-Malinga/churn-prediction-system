from flask import Blueprint, request, jsonify
from application.service import Model_Info_Service
from application.response import response_template, error_response_template

model = Blueprint("model_bp", __name__)

service = Model_Info_Service()

"""
 Add a method to convert all data to dict in models.
"""

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
    
@model.route("/get", methods=["GET"])    
def get_model_info_by_id():
    
    try:
        return response_template(
            "success",
            "Model Information Fetched Successfully",
            service.get_basic_model_info(request.args.get("model_id"))
        ), 200
    except Exception as ex:
        return error_response_template("Failed to fetch Model Information"), 500