from .v1 import data, predict_result, user, dag

def create_routes(app):
    app.register_blueprint(data, url_prefix='/api/v1')
    app.register_blueprint(predict_result, url_prefix='/api/v1')
    app.register_blueprint(user, url_prefix='/api/v1/')
    app.register_blueprint(dag, url_prefix='/api/v1/')