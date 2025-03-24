from marshmallow import Schema, fields

# TODO: Add custom validations
class User_Base_Schema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class User_Register_Schema(User_Base_Schema):
    username = fields.String(required=True)
    
class User_Login_Schema(User_Base_Schema):
    pass