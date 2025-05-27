from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Evaluation_Data_Schema
from application.services import Evaluation_Data_Service
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


data = Blueprint("data_bp", __name__)

service = Evaluation_Data_Service()

@data.route("/", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
# TODO: Complete
def get_data():
    return [], 200



@data.route("/", methods=["POST"])
@limiter.limit("10 per minute")
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
        return error_response_template(
            err.messages
        ), 400
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500


    
@data.route("/list", methods=["POST"])
@limiter.limit("10 per minute")
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
        return error_response_template(
            err.messages
        ), 400  
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500 



@data.route("/csv", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
def read_csv_data():
    data_source = request.files.get("data_source")
    
    if not data_source:
        return error_response_template(
            "No Data Source Uploaded"
        ), 400
        
    file_content_type = data_source.content_type
    
    if file_content_type in ["text/csv"]:
        
        try:
            return response_template(
                "success",
                "CSV Data Source Read Successfully",
                service.preprocess_csv_data(data_source)
            ), 200
        except ValueError as ex:
            return error_response_template(
                f"{ex}"
            ), 400
            
        
    else:
        return error_response_template(
            f"Invalid File type detected: {file_content_type}"
        )


        
@data.route("/info", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
def get_dataset_basic_info():
    try: 
        return response_template(
            "success", 
            "hello", 
            service.basic_dataset_information()
        )
    except SQLAlchemyError as ex:
        return error_response_template(
            f"Database Error: {str(ex)}"
        ), 500
    except Exception as ex:
        return error_response_template(
            f"Server Error: {ex}"
        ), 500