from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from functools import wraps
from flask import current_app
from application.responses.response_template import error_response_template
from requests import HTTPError, RequestException


def apiWrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            current_app.logger.error("Value Error: %s", ex, exc_info=True)
            return error_response_template("Error: Invalid Filtering Value"), 400
        except NoResultFound as ex:
            current_app.logger.error("NotFound error: %s", ex, exc_info=True)
            return error_response_template("No Information found"), 404
        except SQLAlchemyError as ex:
            current_app.logger.error("Database Error: %s", ex, exc_info=True)
            return error_response_template("Error: Database Error Occurred"), 500
        except HTTPError as ex:
            current_app.logger.error("HTTP Error: %s", ex, exc_info=True)
            return (
                error_response_template("Error: Failed to Connect to Airflow Server"),
                500,
            )
        except RequestException as ex:
            current_app.logger.error("Request Error: %s", ex, exc_info=True)
            return (
                error_response_template("Error: Failed to Connect to Airflow Server"),
                500,
            )
        except Exception as ex:
            current_app.logger.error("Unexpected Error: %s", ex, exc_info=True)
            return error_response_template("Error: Server Error Occurred"), 500

    return wrapper
