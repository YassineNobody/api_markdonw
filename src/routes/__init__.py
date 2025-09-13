from flask import Flask
from .category import category_bp
from .reference import reference_bp
from .document import document_bp


def register_blueprints(app: Flask):
    app.register_blueprint(category_bp)
    app.register_blueprint(reference_bp)
    app.register_blueprint(document_bp)
