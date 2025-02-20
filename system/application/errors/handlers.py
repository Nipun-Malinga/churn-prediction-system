from flask import jsonify

def handle_415(error):
    return jsonify(
        {
            "error": "Unsupported media type",
            "message": error.description
        }
    ), 415

def handle_404(error):
    return jsonify(
        {
            "error": "Resource not found",
            "message": error.description
        }
    ), 404

