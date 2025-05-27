import os

import requests
from application.utils import get_csrf_token, login
from requests.exceptions import ConnectionError, HTTPError, RequestException

AIRFLOW_URL = os.getenv("AIRFLOW_URL")
USERNAME = os.getenv("AIRFLOW_USERNAME")
PASSWORD = os.getenv("AIRFLOW_PASSWORD")

class Airflow_Service:
    
    @staticmethod
    def connect_to_airflow():
        """Airflow Connector"""
        try:
            session_cookie, csrf_token = get_csrf_token(AIRFLOW_URL)
            session_cookie = login(AIRFLOW_URL, USERNAME, PASSWORD, session_cookie, csrf_token)
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Cookie": f"session={session_cookie}",  
            }
            
            return headers
        except ConnectionError:
            raise Exception("Failed to connect to Airflow. Ensure the server is running.")
        
    @classmethod
    def fetch_all_dags(cls):
        """Fetch all DAGs from Airflow."""
        try:
            header = cls.connect_to_airflow()
            response = requests.get(f"{AIRFLOW_URL}/api/v1/dags", headers=header)
            response.raise_for_status()
            return response.json()
        except HTTPError as ex:
            raise HTTPError(ex.response.text) from ex
        except RequestException as ex:
            raise RequestException(f"Request error occurred: {str(ex)}") from ex
    
    @classmethod
    def update_dag(cls, dag_id, data):
        """Update a DAG's properties (e.g., is_paused)."""
        try:
            header = cls.connect_to_airflow()
            
            response = requests.patch(
                f"{AIRFLOW_URL}/api/v1/dags/{dag_id}", 
                headers=header, 
                json=data
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as ex:
            raise HTTPError(ex.response.text) from ex
        except RequestException as ex:
            raise RequestException(f"Request error occurred: {str(ex)}") from ex
    
    @classmethod    
    def run_dag(cls, dag_id):
        """ Run Airflow Dag Manually """
        try:
            header = cls.connect_to_airflow()
            response = requests.post(
                f"{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns",
                headers=header,
                json={}
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as ex:
            raise HTTPError(ex.response.text) from ex
        except RequestException as ex:
            raise RequestException(f"Request error occurred: {str(ex)}") from ex