from marshmallow import Schema, fields

class Update_Dag_Schema(Schema):
    is_paused = fields.Boolean(required=True)