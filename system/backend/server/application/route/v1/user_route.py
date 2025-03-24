from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from application.schema import User_Register_Schema, User_Login_Schema
from application.response import response_template, error_response_template
from application.service import save_user, validate_user

user = Blueprint("user_bp", __name__)

@user.route("/register", methods=["POST"])
def register():
    schema = User_Register_Schema()
    
    try:
        requset_data = schema.load(request.json)
        return response_template(
            "success",
            "User registered successfully",
            schema.dump(save_user(requset_data))
        ), 201
        
    except ValidationError as err:
        return error_response_template(err.messages), 400
    
@user.route("/login", methods=["POST"])
def login():
    schema = User_Login_Schema()
    
    try:
        request_data = schema.load(request.json)
        
        if validate_user(request_data): 
            return response_template("success", "User verified successfully", None), 200
        return error_response_template("Invalid Credentials"), 401

    except ValidationError as err:
        return error_response_template(err.messages), 400