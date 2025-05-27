import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

load_dotenv()

DB_NAME = "database.db"

db = SQLAlchemy()
marshmallow = Marshmallow()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["14400 per day", "600 per hour"]
)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    CORS(app)
    JWTManager(app)
    
    db.init_app(app)
    marshmallow.init_app(app)
    limiter.init_app(app)
    
    dictConfig({
        "version": 1.0,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
        },
        "root": {
            "level": "INFO",
            "handlers": ["file", "console"]
        }
    })

    from application.models import (Accuracy_Drift, Data_Transformer,
                                   Data_Transformer_Info, Evaluation_Data,
                                   Model, Model_Hyperparameters, Model_Info,
                                   User, Evaluation_Threshold)

    with app.app_context():
        db.create_all()

    from application.errors import register_error_handler
    from application.routes import create_routes

    create_routes(app)
    register_error_handler(app)

    return app
