from marshmallow import Schema, fields


# TODO: Add custom validations
class Base_Schema(Schema):
    education = fields.String(required=True)
    credit_score = fields.Integer(required=True)
    geography = fields.String(required=True)
    gender = fields.String(required=True)
    age = fields.Integer(required=True)
    tenure = fields.Integer(required=True)
    balance = fields.Float(required=True)
    num_of_products = fields.Integer(required=True)
    has_cr_card = fields.Integer(required=True)
    card_type = fields.String(required=True)
    is_active_member = fields.Integer(required=True)
    estimated_salary = fields.Float(required=True)
    housing = fields.String(required=True)
    loan = fields.String(required=True)
    
class Prediction_Request_Schema(Base_Schema):
    pass

class Evaluation_Data_Schema(Base_Schema):
    exited = fields.Integer(required=True)
