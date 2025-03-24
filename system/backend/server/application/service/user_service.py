from application import db
from application.model import User
from application.schema import User_Login_Schema
from application.util import validate_password

def save_user(data):
    user = User(**data) 
    db.session.add(user)
    db.session.commit()
    return user

def validate_user(data: User_Login_Schema):
    fetched_user = db.session.query(
        User.username,
        User.email,
        User.password
    ).where(User.email == data["email"]).first()
  
    if not fetched_user:
        return False

    return validate_password(data["password"], fetched_user[2])