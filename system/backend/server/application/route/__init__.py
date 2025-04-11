from .v1 import data, predict_result, user, dag, model

def create_routes(app):
    app.register_blueprint(data, url_prefix="/api/v1/data")
    app.register_blueprint(predict_result, url_prefix="/api/v1/predictions")
    app.register_blueprint(user, url_prefix="/api/v1/users")
    app.register_blueprint(dag, url_prefix="/api/v1/airflow")
    app.register_blueprint(model, url_prefix="/api/v1/models")