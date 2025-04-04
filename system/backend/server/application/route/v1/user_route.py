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
        requset_data = schema.load(request.json)
        return response_template(
            "success",
            "User registered successfully",
            schema.dump(service.save_user(requset_data))
        ), 201
        
    except ValidationError as err:
        return error_response_template(err.messages), 400
    
@user.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    schema = User_Login_Schema()
    
    try:
        request_data = schema.load(request.json)
        
        if service.validate_user(request_data): 
            return response_template("success", "User verified successfully", None), 200
        return error_response_template("Invalid Credentials"), 401

    except ValidationError as err:
        return error_response_template(err.messages), 400