# src/__init__.py
from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.extensions import db, migrate
from src.routes import register_blueprints
from src import errors

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    errors.register_error_handlers(app)

    return app
