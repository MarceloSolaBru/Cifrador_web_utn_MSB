from flask import Flask
from flask_marshmallow import Marshmallow
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config

from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()

def create_app() -> Flask:
    app_context = os.getenv("FLASK_CONTEXT")
    print(f"app_context: {app_context}")

    app = Flask(__name__)

    config_instance = config.factory(app_context if app_context else "development")
    app.config.from_object(config_instance)

    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.resources import home, user, auth

    app.register_blueprint(home, url_prefix="/api/v1")
    app.register_blueprint(user, url_prefix="/api/v1")
    app.register_blueprint(auth, url_prefix='/api/v1/auth')

    @app.shell_context_processor
    def shell_context():
        return {"app": app}

    return app
