from application import limiter
from application.response import error_response_template, response_template
from application.schema import Update_Dag_Schema
from application.service import Airflow_Service
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from requests import HTTPError, RequestException

dag = Blueprint("dag_bp", __name__)

service = Airflow_Service()

@dag.route("/dags", methods=["GET"])
@limiter.limit("5 per minute")
@jwt_required()
def fetch_all():
    try:
        dags = service.fetch_all_dags()
        return response_template(
            "success", 
            "DAG data fetched successfully", 
            dags
        ), 200
    except HTTPError as ex:
            error_response_template(str(ex)), 500
    except RequestException as ex:
            error_response_template(str(ex)), 500  
    except Exception as ex:
        return error_response_template(str(ex)), 500



@dag.route("/dags", methods=["PATCH"])
@limiter.limit("5 per minute")
@jwt_required()
def pause_dag():
    schema = Update_Dag_Schema()
    try:
        dag_id = request.args.get("dag_id")
        if not dag_id:
            return error_response_template("Missing dag_id in query parameters"), 400

        dag_data = service.update_dag(
            dag_id,
            schema.load(request.json)
        )
        return response_template("success", "DAG data fetched successfully", dag_data), 200
    except ValidationError as exp:
        return error_response_template(str(exp)), 400
    except HTTPError as ex:
            error_response_template(str(ex)), 500
    except RequestException as ex:
            error_response_template(str(ex)), 500  
    except Exception as exp:
        return error_response_template(str(exp)), 500



@dag.route("/dags", methods=["POST"])    
@limiter.limit("5 per minute")
@jwt_required()
def run_dag():
    try:
        dag_id = request.args.get("dag_id")
        if not dag_id:
            return error_response_template("Missing dag_id in query parameters"), 400
        
        dag = service.run_dag(
            request.args.get("dag_id"),
        )
        return response_template("success", "DAG data fetched successfully", dag), 200
    except ValidationError as exp:
        return error_response_template(str(exp)), 400
    except HTTPError as ex:
            error_response_template(str(ex)), 500
    except RequestException as ex:
            error_response_template(str(ex)), 500  
    except Exception as exp:
        return error_response_template(str(exp)), 500    
