from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from functools import wraps
from flask import current_app
from application.responses.response_template import error_response_template
from application.exceptions import (
    AirflowConnectionError,
    AirflowLoginError,
    AirflowCSRFError,
    AirflowAPIError,
)
from werkzeug.exceptions import NotFound

def apiWrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            current_app.logger.error(f"Value Error: {ex}")
            return error_response_template("Error: Invalid Filtering Value"), 400
        except NoResultFound as ex:
            current_app.logger.info(f"Resource Not Found: {ex}")
            return error_response_template("No Information Found"), 404
        except TypeError as ex:
            current_app.logger.error(f"Type Error: {ex}")
            return error_response_template("Error: Type Error"), 500
        except SQLAlchemyError as ex:
            current_app.logger.error(f"Database Error: {ex}")
            return error_response_template("Error: Database Error Occurred"), 500
        except NotFound as ex:
            current_app.logger.warning(f"File Not Found: {ex}")
            return error_response_template("Error: Database Error Occurred"), 404
        except (
            AirflowConnectionError,
            AirflowLoginError,
            AirflowCSRFError,
            AirflowAPIError,
        ) as ex:
            current_app.logger.error(f"Airflow Service Unavailable Error: {ex}")
            return error_response_template(f"Error: Airflow Service Not Available"), 503
        except Exception as ex:
            current_app.logger.error(f"Unexpected Error: {ex}")
            return (
                error_response_template("Error: Unexpected Server Error Occurred"),
                500,
            )

    return wrapper
