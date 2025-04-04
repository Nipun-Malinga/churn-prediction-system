from flask import Blueprint, request, jsonify
from application import limiter
from application.service import Airflow_Service
from application.response import response_template, error_response_template

dag = Blueprint("dag_bp", __name__)

service = Airflow_Service()

@dag.route("/dags", methods=["GET"])
@limiter.limit("5 per minute")
def fetch_all():
    try:
        dags = service.fetch_all_dags()
        return response_template("success", "DAG data fetched successfully", dags), 200
    except Exception as ex:
        return error_response_template(str(ex)), 500