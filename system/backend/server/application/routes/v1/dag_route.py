from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Update_Dag_Schema
from application.services import Airflow_Service
from application.wrappers import apiWrapper
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from requests import HTTPError, RequestException

dag = Blueprint("dag_bp", __name__)

service = Airflow_Service()


@dag.route("/dags", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def fetch_all():
    dags = service.fetch_all_dags()
    current_app.logger.info("Dag Info Fetched Successfully")

    return response_template("success", "DAG data fetched successfully", dags), 200


@dag.route("/dags", methods=["PATCH"])
@limiter.limit("10 per minute")
@jwt_required()
@apiWrapper
def pause_dag():
    schema = Update_Dag_Schema()
    dag_id = request.args.get("dag_id")
    if not dag_id:
        return error_response_template("Missing dag_id in query parameters"), 400
    dag_data = service.update_dag(dag_id, schema.load(request.json))
    current_app.logger.info("Dag Updated Successfully")

    return response_template("success", "DAG data fetched successfully", dag_data), 200


@dag.route("/dags", methods=["POST"])
@limiter.limit("10 per minute")
@jwt_required()
def run_dag():
    dag_id = request.args.get("dag_id")
    if not dag_id:
        return error_response_template("Missing dag_id in query parameters"), 400

    dag = service.run_dag(
        request.args.get("dag_id"),
    )
    current_app.logger.info("Dag Ran Successfully")

    return response_template("success", "DAG data fetched successfully", dag), 200
