from .v1.evaluation_data_route import data

def create_routes(app):
    app.register_blueprint(data, url_prefix='/api/v1')