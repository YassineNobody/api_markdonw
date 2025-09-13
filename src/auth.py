from functools import wraps
from flask import request, jsonify, current_app

def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        
        token = auth_header.split(" ")[1]
        if token != current_app.config["API_SECRET_TOKEN"]:
            return jsonify({"error": "Forbidden"}), 403
        
        return f(*args, **kwargs)
    return decorated
