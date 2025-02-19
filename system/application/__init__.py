import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "database.db"

db = SQLAlchemy()
marshmallow = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    marshmallow.init_app(app)

    from application.model import Model, Model_Info, Accuracy_Drift, Evaluation_Data

    with app.app_context():
        db.create_all()

    from application.route import create_routes
    from application.errors import register_error_handler

    create_routes(app)
    register_error_handler(app)

    return app
