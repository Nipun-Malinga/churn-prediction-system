from flask import jsonify

def handle_415(error):
    return jsonify(
        {
            "error": "Unsupported media type",
            "message": "Send JSON data with 'Content-Type: application/json'"
        }
    ), 415

def handle_404(error):
    return jsonify(
        {
            "error": "Not found",
            "message": "The requested resource was not found"
        }
    ), 404

