from flask import request, jsonify, current_app
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not current_app.config.get("API_KEYS") or key not in current_app.config["API_KEYS"]:
            current_app.logger.warning(f"Percobaan kunci API tidak sah: {key} dari {request.remote_addr}")
            return jsonify({"error": "Tidak berwenang"}), 401
        return f(*args, **kwargs)
    return decorator