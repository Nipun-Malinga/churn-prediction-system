from application import limiter
from application.responses import error_response_template, response_template
from application.schemas import User_Login_Schema, User_Register_Schema
from application.services import User_Service
from flask import Blueprint, request, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

user = Blueprint("user_bp", __name__)

service = User_Service()


@user.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    schema = User_Register_Schema()

    auth_token = service.save_user(schema.load(request.json))
    current_app.logger.info("User Email Registered Successfully")

    return (
        response_template(
            "success", "User registered successfully", {"auth_token": auth_token}
        ),
        201,
    )


@user.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    schema = User_Login_Schema()

    auth_token = service.validate_user(schema.load(request.json))
    current_app.logger.info("User Email Validated Successfully")

    if auth_token:
        return (
            response_template(
                "success", "User verified successfully", {"auth_token": auth_token}
            ),
            200,
        )
    return error_response_template("Invalid Credentials"), 401
