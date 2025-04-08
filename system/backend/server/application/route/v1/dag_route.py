from application import limiter
from application.response import error_response_template, response_template
from application.schema import Update_Dag_Schema
from application.service import Airflow_Service
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

dag = Blueprint("dag_bp", __name__)

service = Airflow_Service()

@dag.route("/dags", methods=["GET"])
@limiter.limit("5 per minute")
@jwt_required()
def fetch_all():
    try:
        dags = service.fetch_all_dags()
        return response_template("success", "DAG data fetched successfully", dags), 200
    except Exception as exp:
        return error_response_template(str(exp)), 500

@dag.route("/dags", methods=["PATCH"])
@limiter.limit("5 per minute")
@jwt_required()
def pause_dag():
    schema = Update_Dag_Schema()
    try:
        dag = service.update_dag(
            request.args.get("dag_id"),
            schema.load(request.json)
        )
        return response_template("success", "DAG data fetched successfully", dag), 200
    except ValidationError as exp:
        return error_response_template(str(exp)), 400
    except Exception as exp:
        return error_response_template(str(exp)), 500

@dag.route("/dags", methods=["POST"])    
@limiter.limit("5 per minute")
@jwt_required()
def run_dag():
    try:
        dag = service.run_dag(
            request.args.get("dag_id"),
        )
        return response_template("success", "DAG data fetched successfully", dag), 200
    except ValidationError as exp:
        return error_response_template(str(exp)), 400
    except Exception as exp:
        return error_response_template(str(exp)), 500    
