from flask import jsonify


def handle_400(error):
    return jsonify(
        {
            "error": "Resource not found",
            "message": error.description
        }
    ), 400

def handle_404(error):
    return jsonify(
        {
            "error": "Resource not found",
            "message": error.description
        }
    ), 404

def handle_405(error):
    return jsonify(
        {
            "error": "Method not allowed",
            "message": error.description
        }
    ), 405

def handle_415(error):
    return jsonify(
        {
            "error": "Unsupported media type",
            "message": error.description
        }
    ), 415
    
def handle_429(error):
    return jsonify(
        {
            "error": "Too Many Requests",
            "message": error.description
        }
    ), 429


def handle_500(error):
    return jsonify(
        {
            "error": "Internal server error",
            "message": error.description
        }
    ), 500