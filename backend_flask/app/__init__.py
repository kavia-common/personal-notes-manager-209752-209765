from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from .config import Config
from .models import db
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.notes import blp as notes_blp


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance with:
        - SQLAlchemy and SQLite database initialized and auto-created
        - JWT authentication enabled
        - Blueprint routes registered under / and /api
        - OpenAPI documentation served under /docs
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load config
    app.config.from_object(Config)

    # CORS
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)  # noqa: F841

    # API and docs
    api = Api(app)

    # Register blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(notes_blp)

    # Auto-create DB if not exists
    with app.app_context():
        db.create_all()

    return app


# Keep default app variable for existing run.py import
app = create_app()
