from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from application import db
from application.schema import Evaluation_Data_Schema
from application.model import Evaluation_Data
from application.response import response_template, error_response_template

data = Blueprint('data_bp', __name__)

@data.route('/data', methods=['GET'])
# TODO: Complete
def get_data():
    return [], 200

@data.route('/data', methods=['POST'])
def add_data():
    schema = Evaluation_Data_Schema()

    try:
        request_data = schema.load(request.json)
        new_entry = Evaluation_Data(**request_data)

        db.session.add(new_entry)
        db.session.commit()
        
        return response_template('success', 'New data added to the server successfully', schema.dump(new_entry)), 201
    except ValidationError as err:
        return error_response_template(err.messages), 400