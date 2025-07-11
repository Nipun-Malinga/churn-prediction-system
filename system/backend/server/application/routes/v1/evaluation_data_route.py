from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Evaluation_Data_Schema
from application.services import Evaluation_Data_Service
from application.wrappers import apiWrapper
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


data = Blueprint("data_bp", __name__)

service = Evaluation_Data_Service()


@data.route("/", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
# TODO: Complete
def get_data():
    return [], 200


@data.route("/", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def add_data():
    schema = Evaluation_Data_Schema()
    request_data = schema.load(request.json)
    saved_data = service.save_evaluation_data(request_data)
    current_app.logger.info("Evaluation Data Added Successfully")

    return (
        response_template(
            "success",
            "New data added to the server successfully",
            schema.dump(saved_data),
        ),
        201,
    )


@data.route("/list", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def add_data_list():
    schema = Evaluation_Data_Schema(many=True)
    request_data = schema.load(request.json)
    saved_entries = [service.save_evaluation_data(entry) for entry in request_data]
    current_app.logger.info("Evaluation Data Added Successfully")

    return (
        response_template(
            "success",
            f"{len(saved_entries)} new data entries added successfully",
            schema.dump(saved_entries),
        ),
        201,
    )


@data.route("/csv", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def read_csv_data():
    data_source = request.files.get("data_source")

    if not data_source:
        return error_response_template("No Data Source Uploaded"), 400

    file_content_type = data_source.content_type

    if file_content_type in ["text/csv"]:
        saved_entities = service.save_csv_evaluation_data(data_source)
        current_app.logger.info("Evaluation Data CSV Added Successfully")

        return (
            response_template(
                "success", "CSV Data Source Read Successfully", saved_entities
            ),
            201,
        )

    else:
        return (
            error_response_template(f"Invalid File type detected: {file_content_type}"),
            400,
        )


@data.route("/info", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_dataset_basic_info():
    current_app.logger.info("Basic Dataset Info Fetched Successfully")
    return response_template("success", "hello", service.basic_dataset_information())
