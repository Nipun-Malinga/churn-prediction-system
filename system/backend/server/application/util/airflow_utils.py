import re
import requests

def get_csrf_token(url):
    """Get the CSRF token from the login page response"""
    response = requests.get(url + "/login/")
    pattern = r'<input(?:\s+(?:(?:type|name|id)\s*=\s*"[^"]*"\s*)+)?\s+value="([^"]+)">'
    csrf_token = re.search(pattern, response.text)
    initial_session_cookie = response.cookies.get('session')

    if csrf_token:
        print("[+] CSRF token found.")
        return initial_session_cookie, csrf_token.group(1)
    else:
        print("[-] CSRF token not found. Exiting...")
        exit(1)
        
def login(url, username, password, cookie, csrf_token):
    """Login to the Apache Airflow web application"""
    response = requests.post(
        url + "/login/",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"session={cookie}"
        },
        data={"csrf_token": csrf_token, "username": username, "password": password}
    )

    if "Invalid login. Please try again." in response.text:
        print("[+] Login was not successful due to invalid credentials.")
        exit(1)

    elif response.status_code != 200:
        print("[-] Something went wrong with the login process.")

    elif "Set-Cookie" in response.headers:
        session_cookie = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
        print(f"Login was successful. Captured session cookie: {session_cookie}")
        return session_cookie