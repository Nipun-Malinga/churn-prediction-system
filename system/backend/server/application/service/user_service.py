import json
from application import db
from application.model import User
from application.schema import User_Login_Schema
from application.util import validate_password
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

class User_Service:

    @classmethod
    def save_user(cls, data):
        try:
            user = User(**data) 
            db.session.add(user)
            db.session.commit()
            return create_access_token(
                identity={"user_id:": user.id}, 
                additional_claims={"email": user.email}
            )
        except IntegrityError as exp:
            db.session.rollback()  
            raise ValueError()
            

    @classmethod
    def validate_user(cls, data: User_Login_Schema):
        fetched_user = db.session.query(
            User.id,
            User.username,
            User.email,
            User.password
        ).where(User.email == data["email"]).first()
        
        try:
            if not fetched_user or not validate_password(data["password"], fetched_user[3]):
                return None
        except ValueError as exp:
            raise ValueError("User validation failed due to password error") from exp
        
        return create_access_token(
                identity={"user_id:": fetched_user[0]},
                additional_claims={"email": fetched_user[2]}
        )