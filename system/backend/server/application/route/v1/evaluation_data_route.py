from application import limiter
from application.response import error_response_template, response_template
from application.schema import Evaluation_Data_Schema
from application.service import Evaluation_Data_Service
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

data = Blueprint("data_bp", __name__)

service = Evaluation_Data_Service()

@data.route("/", methods=["GET"])
@limiter.limit("5 per minute")
@jwt_required()
# TODO: Complete
def get_data():
    return [], 200

@data.route("/", methods=["POST"])
@limiter.limit("5 per minute")
@jwt_required()
def add_data():
    schema = Evaluation_Data_Schema()

    try:
        request_data = schema.load(request.json)
        return response_template(
            "success", 
            "New data added to the server successfully", 
            schema.dump(service.save_evaluation_data(request_data))
        ), 201

    except ValidationError as err:
        return error_response_template(err.messages), 400
    
@data.route("/list", methods=["POST"])
@limiter.limit("5 per minute")
@jwt_required()
def add_data_list():
    schema = Evaluation_Data_Schema(many=True)

    try:
        request_data = schema.load(request.json) 
        saved_entries = [service.save_evaluation_data(entry) for entry in request_data]
        
        return response_template(
            "success", 
            f"{len(saved_entries)} new data entries added successfully", 
            schema.dump(saved_entries)
        ), 201

    except ValidationError as err:
        return error_response_template(err.messages), 400   

@data.route("/csv", methods=["POST"])
@limiter.limit("5 per minute")
@jwt_required()
def add_csv_data():
    return

@data.route("/csv/read", methods=["POST"])
@limiter.limit("5 per minute")
@jwt_required()
def read_csv_data():
    return   