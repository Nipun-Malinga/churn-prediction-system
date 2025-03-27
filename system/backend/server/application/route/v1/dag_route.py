from flask import Blueprint, request, jsonify
from application.service import fetch_all_dags
from application.response import response_template, error_response_template

dag = Blueprint("dag_bp", __name__)

@dag.route("/dags", methods=["GET"])
def fetch_all():
    return response_template(
        "success",
        "Dag data fetched successfully",
        fetch_all_dags()
    )