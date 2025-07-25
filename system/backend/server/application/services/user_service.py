import json

from flask import current_app

from application import db
from application.models import User
from application.schemas import User_Login_Schema
from application.utils import validate_password
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from application.exceptions import UserAlreadyRegisteredException, UserNotFoundException


class User_Service:

    @classmethod
    def save_user(cls, data):
        try:
            user = User(**data) 
            db.session.add(user)
            db.session.commit()
            return create_access_token(
                identity=json.dumps({"user_id": user.id}), 
                additional_claims={"email": user.email}
            )
        except IntegrityError as ex:
            db.session.rollback()  
            current_app.logger.warning(f"Integrity Error Occurred While Saving User: {ex}")
            raise UserAlreadyRegisteredException("User Already Exists In The System")
        except SQLAlchemyError as ex:
            db.session.rollback()  
            current_app.logger.error("SQLAlchemy Error Occurred While Saving User")
            raise RuntimeError("Database Error Occurred While Saving User") from ex
            

    @classmethod
    def validate_user(cls, data: User_Login_Schema):
        try:
            fetched_user = db.session.query(
                User.id,
                User.username,
                User.email,
                User.password
            ).where(User.email == data["email"]).first()
            
            if not fetched_user:
                raise UserNotFoundException("User Not Found")
            
            if not fetched_user or not validate_password(data["password"], fetched_user[3]):
                return None
            
            return create_access_token(
                identity=json.dumps({"user_id:": fetched_user[0]}), 
                additional_claims={"email": fetched_user[2]}
            )
            
        except SQLAlchemyError as ex:
            current_app.logger.error("SQLAlchemy Error While Retrieving User Information")
            raise SQLAlchemyError("An Error While Retrieving User Information") from ex
        except ValueError as ex:
            current_app.logger.error("User Validation Failed Due to Password Error")
            raise ValueError("User validation Failed") from ex