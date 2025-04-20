import json

from application import db
from application.model import User
from application.schema import User_Login_Schema
from application.util import validate_password
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class User_Service:

    @classmethod
    def save_user(cls, data):
        try:
            user = User(**data) 
            db.session.add(user)
            db.session.commit()
            return create_access_token(
                identity=json.dumps({"user_id:": user.id}), 
                additional_claims={"email": user.email}
            )
        except IntegrityError as ex:
            db.session.rollback()  
            raise ValueError()
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while saving user information."
            ) from ex
            

    @classmethod
    def validate_user(cls, data: User_Login_Schema):
        try:
            fetched_user = db.session.query(
                User.id,
                User.username,
                User.email,
                User.password
            ).where(User.email == data["email"]).first()
            
            if not fetched_user or not validate_password(data["password"], fetched_user[3]):
                return None
            
            return create_access_token(
                identity=json.dumps({"user_id:": fetched_user[0]}), 
                additional_claims={"email": fetched_user[2]}
            )
            
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving user information."
            ) from ex
        except ValueError as ex:
            raise ValueError(
                "User validation failed due to password error"
            ) from ex