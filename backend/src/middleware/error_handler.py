from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_exception(e):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    else:
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "description": "An unexpected error occurred.",
        }), 500

# In your main Flask app file:
app.register_error_handler(Exception, handle_exception)
