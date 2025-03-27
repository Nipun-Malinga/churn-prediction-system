import requests
from application.util import get_csrf_token, login

def fetch_all_dags():
    airflow_url = "http://127.0.0.1:8080/"
    session_cookie, csrf_token = get_csrf_token(airflow_url)
    session_cookie = login(
        airflow_url,"admin","nipun1244744",
        session_cookie,
        csrf_token
    )
    
    endpoint = f'{airflow_url}/api/v1/dags'
    headers = {'Cookie': f'session={session_cookie}'}
    response = requests.get(endpoint, headers=headers)
    response_data = response.json()

    return response_data