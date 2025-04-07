from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from application import limiter
from application.schema import User_Register_Schema, User_Login_Schema
from application.response import response_template, error_response_template
from application.service import User_Service

user = Blueprint("user_bp", __name__)

service = User_Service()

@user.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    schema = User_Register_Schema()
    
    try:
        auth_token = service.save_user(schema.load(request.json))   
        return response_template(
            "success",
            "User registered successfully",
            {
                "auth_token": auth_token
            }
        ), 201
        
    except ValidationError as exp:
        return error_response_template(exp.messages), 400
    except ValueError as exp:
        return error_response_template(
            "User could not be saved. Possible duplicate or constraint violation."
        ), 409
    
@user.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    schema = User_Login_Schema()
    
    try:
        auth_token = service.validate_user(schema.load(request.json))
        
        if auth_token: 
            return response_template(
                "success", 
                "User verified successfully", 
                {
                    "auth_token": auth_token
                }
            ), 200
        return error_response_template("Invalid Credentials"), 401

    except ValidationError as exp:
        return error_response_template(exp.messages), 400
    except ValueError as exp:
        return error_response_template("Failed to authenticate user"), 500