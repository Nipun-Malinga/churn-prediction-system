from enum import Enum
from application.wrappers import apiWrapper
from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Evaluation_Threshold_Schema
from application.services import Model_Info_Service
from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

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
@apiWrapper
def get_models():
    models = service.get_all_models()
    current_app.logger.info("Models Fetched Successfully")

    return response_template("success", "Models Fetched Successfully", models), 200


@model.route("/info", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_basic_model():
    basic_model_info = service.get_basic_model_info()
    current_app.logger.info("Model Info Fetched Successfully")

    return (
        response_template(
            "success", "Model Information Fetched Successfully", basic_model_info
        ),
        200,
    )


@model.route("/info/advanced", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_advanced_model_info_by_id():
    model_id = request.args.get("model_id")
    advanced_model_info = service.get_advanced_model_info(model_id)
    current_app.logger.info("Advanced Model Info Fetched Successfully")

    return (
        response_template(
            "success", "Model Information Fetched Successfully", advanced_model_info
        ),
        200,
    )


@model.route("/base", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_base_model_performance():
    base_model_performance = service.get_base_model_performance()
    current_app.logger.info("Base Model Performance Fetched Successfully")

    return (
        response_template(
            "success", "Base Model Data Successfully", base_model_performance
        ),
        200,
    )


@model.route("/charts", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def model_history_chart_data():
    model_id = request.args.get("model_id")
    filter_by = request.args.get("filter_type")
    if not model_id:
        return error_response_template("Missing required parameters"), 400
    Type(filter_by)

    chart_data = service.model_performance_history(model_id, filter_by)
    current_app.logger.info(
        "Chart Data Fetched Successfully for Model ID %s with filter %s",
        model_id,
        filter_by,
    )

    return response_template(
        "success",
        f"Model Id: {model_id}, Filter: {filter_by.capitalize()} Data Fetched Successfully",
        chart_data,
    )


def get_base_model_performance_data():
    None


@model.route("/drift", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_model_performance_drift():
    drift_history = service.model_drift_history()
    current_app.logger.info(
        "Model Performance Drift History Chart Data Fetched Successfully"
    )

    return (
        response_template(
            "success", "Drift History Fetched Successfully", drift_history
        ),
        200,
    )


@model.route("/production", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_new_trained_models():
    new_trained_models = service.new_trained_models()
    current_app.logger.info("New Trained Models Fetched Successfully")

    return (
        response_template(
            "success", "New Trained Models Fetched Successfully", new_trained_models
        ),
        200,
    )


@model.route("/production", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def set_production_model():
    batch_id = request.args.get("batch_id")

    if not batch_id:
        return error_response_template("Missing required parameters"), 400

    production_model = service.production_model(batch_id)
    current_app.logger.info(
        "New Production Model Set Successfully. Batch Id: %s", batch_id
    )

    return response_template(
        "success", "Production Models Set Successfully", production_model
    )


@model.route("/evaluation-threshold", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def set_evaluation_threshold():
    schema = Evaluation_Threshold_Schema()
    request_data = schema.load(request.json)

    set_threshold = service.set_threshold(request_data)
    current_app.logger.info(
        "New Drift Evaluation Threshold Set Successfully. Threshold: %s", set_threshold
    )

    return (
        response_template(
            "success",
            "Evaluation thresholds set successfully",
            schema.dump(set_threshold),
        ),
        201,
    )


@model.route("/evaluation-threshold", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def get_evaluation_threshold():
    threshold = service.get_threshold()
    current_app.logger.info("Threshold Fetched Successfully")

    return (
        response_template(
            "success", "Evaluation thresholds fetched successfully", threshold
        ),
        201,
    )
