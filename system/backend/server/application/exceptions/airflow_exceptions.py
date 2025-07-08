# application/exceptions.py
class AirflowConnectionError(Exception):
    pass

class AirflowLoginError(Exception):
    pass

class AirflowCSRFError(Exception):
    pass

class AirflowAPIError(Exception):
    pass
