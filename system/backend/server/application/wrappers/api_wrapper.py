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


def apiWrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            current_app.logger.error("Value Error: %s", ex, exc_info=False)
            return error_response_template("Error: Invalid Filtering Value"), 400
        except NoResultFound as ex:
            current_app.logger.error("NotFound error: %s", ex, exc_info=False)
            return error_response_template("No Information found"), 404
        except SQLAlchemyError as ex:
            current_app.logger.error("Database Error: %s", ex, exc_info=False)
            return error_response_template("Error: Database Error Occurred"), 500
        except (AirflowConnectionError, AirflowLoginError, AirflowCSRFError) as ex:
            current_app.logger.error("Airflow Auth Error: %s", ex, exc_info=False)
            return error_response_template(str(ex)), 500
        except AirflowAPIError as ex:
            current_app.logger.error("Airflow API Error: %s", ex, exc_info=False)
            return error_response_template(str(ex)), 500
        except Exception as ex:
            current_app.logger.error("Unexpected Error: %s", ex, exc_info=False)
            return error_response_template("Error: Server Error Occurred"), 500

    return wrapper
