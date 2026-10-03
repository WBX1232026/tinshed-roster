"""Flask entry point for the Tinshed Roster web application.

Run with: python -m flask --app src.app run
"""

from flask import Flask

from src.views import views_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(views_bp)
    return app


app = create_app()
