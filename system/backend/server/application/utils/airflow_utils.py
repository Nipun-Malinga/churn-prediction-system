import re

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException


def get_csrf_token(url):
    """Get the CSRF token from the login page response."""
    try:
        response = requests.get(url + "/login/")
        response.raise_for_status()

        pattern = r'<input(?:\s+(?:(?:type|name|id)\s*=\s*"[^"]*"\s*)+)?\s+value="([^"]+)">'
        csrf_token = re.search(pattern, response.text)
        initial_session_cookie = response.cookies.get("session")

        if csrf_token:
            return initial_session_cookie, csrf_token.group(1)
        else:
            raise Exception("CSRF token not found.")
    except RequestException:
        raise Exception("Failed to connect to Airflow.")
        
def login(url, username, password, cookie, csrf_token):
    """Login to the Apache Airflow web application."""
    try:
        response = requests.post(
            url + "/login/",
            headers={"Content-Type": "application/x-www-form-urlencoded", "Cookie": f"session={cookie}"},
            data={"csrf_token": csrf_token, "username": username, "password": password},
        )
        response.raise_for_status()

        if "Invalid login" in response.text:
            raise Exception("Invalid login credentials.")

        return response.cookies.get("session")
    except RequestException:
        raise Exception("Failed to log in to Airflow.")