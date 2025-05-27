from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import Update_Dag_Schema
from application.services import Airflow_Service
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from requests import HTTPError, RequestException

dag = Blueprint("dag_bp", __name__)

service = Airflow_Service()

@dag.route("/dags", methods=["GET"])
@limiter.limit("10 per minute")
@jwt_required()
def fetch_all():
    try:
        dags = service.fetch_all_dags()
        current_app.logger.info("Dag Info Fetched Successfully")
        
        return response_template(
            "success", 
            "DAG data fetched successfully", 
            dags
        ), 200
    except HTTPError as ex:
        current_app.logger.error("HTTP Error: %s", ex, exc_info=True)
        return error_response_template("Error: Failed to Connect to Airflow Server"), 500
    except RequestException as ex:
        current_app.logger.error("Request Error: %s", ex, exc_info=True)
        return error_response_template("Error: Failed to Connect to Airflow Server"), 500 
    except Exception as ex:
        current_app.logger.error("Unexpected Error: %s", ex, exc_info=True)
        return error_response_template("Error: Server Error Occurred"), 500



@dag.route("/dags", methods=["PATCH"])
@limiter.limit("10 per minute")
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
        current_app.logger.info("Dag Updated Successfully")
        
        return response_template("success", "DAG data fetched successfully", dag_data), 200
    except ValidationError as ex:
        current_app.logger.error("Validation Error: %s", ex, exc_info=True)
        return error_response_template(ex.messages), 400 
    except HTTPError as ex:
        current_app.logger.error("HTTP Error: %s", ex, exc_info=True)
        return error_response_template("Error: Failed to Connect to Airflow Server"), 500
    except RequestException as ex:
        current_app.logger.error("Request Error: %s", ex, exc_info=True)
        return error_response_template("Error: Failed to Connect to Airflow Server"), 500 
    except Exception as exp:
        current_app.logger.error("Unexpected Error: %s", ex, exc_info=True)
        return error_response_template("Error: Server Error Occurred"), 500



@dag.route("/dags", methods=["POST"])    
@limiter.limit("10 per minute")
@jwt_required()
def run_dag():
    try:
        dag_id = request.args.get("dag_id")
        if not dag_id:
            return error_response_template("Missing dag_id in query parameters"), 400
        
        dag = service.run_dag(
            request.args.get("dag_id"),
        )
        current_app.logger.info("Dag Ran Successfully")
        
        return response_template("success", "DAG data fetched successfully", dag), 200
    except ValidationError as ex:
        current_app.logger.error("Validation Error: %s", ex, exc_info=True)
        return error_response_template(ex.messages), 400 
    except HTTPError as ex:
        current_app.logger.error("HTTP Error: %s", ex, exc_info=True)
        return error_response_template("Error: Failed to Connect to Airflow Server"), 500
    except RequestException as ex:
        current_app.logger.error("Request Error: %s", ex, exc_info=True)
        return error_response_template("Error: Failed to Connect to Airflow Server"), 500 
    except Exception as exp:
        current_app.logger.error("Unexpected Error: %s", ex, exc_info=True)
        return error_response_template("Error: Server Error Occurred"), 500   
