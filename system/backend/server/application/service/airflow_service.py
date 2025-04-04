import requests
import os
from application.util import get_csrf_token, login
from requests.exceptions import ConnectionError, HTTPError, RequestException

AIRFLOW_URL = os.getenv("AIRFLOW_URL")
USERNAME = os.getenv("AIRFLOW_USERNAME")
PASSWORD = os.getenv("AURFLOW_PASSWORD")

class Airflow_Service:

    @classmethod
    def fetch_all_dags(cls):
        """Fetch all DAGs from Airflow."""
        try:
            session_cookie, csrf_token = get_csrf_token(AIRFLOW_URL)
            session_cookie = login(AIRFLOW_URL, USERNAME, PASSWORD, session_cookie, csrf_token)

            headers = {"Cookie": f"session={session_cookie}"}
            response = requests.get(f"{AIRFLOW_URL}/api/v1/dags", headers=headers)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            raise Exception("Failed to connect to Airflow. Ensure the server is running.")
        except HTTPError:
            raise Exception("HTTP error occurred while fetching DAGs.")
        except RequestException:
            raise Exception("An error occurred while making the request.")
