from marshmallow import Schema, fields

class Evaluation_Threshold_Schema(Schema):
    accuracy = fields.Integer(required=True)
    precision = fields.Integer(required=True)
    recall = fields.Integer(required=True)
    f1_score = fields.Integer(required=True)
