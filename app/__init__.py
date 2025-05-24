from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    origins = app.config.get("CORS_ORIGINS", "*")
    CORS(app, resources={"/*": {"origins": origins}})

    rate_limit_string = app.config.get("RATELIMIT_DEFAULT")
    if not rate_limit_string:
        rate_limit_string = "5 per minute"

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        storage_uri="memory://",
        default_limits=[rate_limit_string],
    )

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        return jsonify({
            "error": "batas permintaan terlampaui",
            "message": str(e.description),
            "limit": str(e.limit.limit) if e.limit else "N/A"
        }), 429

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

