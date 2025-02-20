from .handlers import handle_415, handle_404

def register_error_handler(app):
    app.register_error_handler(415, handle_415)
    app.register_error_handler(404, handle_404)