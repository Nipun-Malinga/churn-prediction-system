from flask import Blueprint, request, jsonify
from application.service import fetch_all_dags
from application.response import response_template, error_response_template

dag = Blueprint("dag_bp", __name__)

@dag.route("/dags", methods=["GET"])
def fetch_all():
    try:
        dags = fetch_all_dags()
        return response_template("success", "DAG data fetched successfully", dags), 200
    except Exception as ex:
        return error_response_template(str(ex)), 500