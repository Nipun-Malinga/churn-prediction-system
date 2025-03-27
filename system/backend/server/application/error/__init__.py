from .handlers import (handle_400, handle_404, handle_405, handle_415,
                       handle_429, handle_500)


def register_error_handler(app):
    app.register_error_handler(400, handle_400)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(405, handle_405)
    app.register_error_handler(415, handle_415)
    app.register_error_handler(429, handle_429)
    app.register_error_handler(500, handle_500)