import json

from flask import current_app

from application import db
from application.models import User
from application.schemas import User_Login_Schema
from application.utils import validate_password
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
                identity=json.dumps({"user_id": user.id}), 
                additional_claims={"email": user.email}
            )
        except IntegrityError as ex:
            db.session.rollback()  
            current_app.logger.warning(f"Integrity Error Occurred While Saving User: {ex}", exc_info=True)
            raise ValueError("User Already Exists or Violates Unique Constraint.") from ex
        except SQLAlchemyError as ex:
            db.session.rollback()  
            current_app.logger.error("SQLAlchemy Error Occurred While Saving User", exc_info=True)
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
            
            if not fetched_user or not validate_password(data["password"], fetched_user[3]):
                return None
            
            return create_access_token(
                identity=json.dumps({"user_id:": fetched_user[0]}), 
                additional_claims={"email": fetched_user[2]}
            )
            
        except SQLAlchemyError as ex:
            current_app.logger.error("SQLAlchemy Error While Retrieving User Information", exc_info=True)
            raise SQLAlchemyError("An Error While Retrieving User Information") from ex
        except ValueError as ex:
            current_app.logger.error("User Validation Failed Due to Password Error", exc_info=True)
            raise ValueError("User validation Failed") from ex