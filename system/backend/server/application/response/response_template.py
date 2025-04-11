from flask import jsonify


def response_template(status, message, data):
    return jsonify(
        {
            "status": status,
            "message": message,
            "data": data
        }
    )

def error_response_template(message):
    return jsonify(
        {
            "status": 'failed',
            "message": message
        }
    )