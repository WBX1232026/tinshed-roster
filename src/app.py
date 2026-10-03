"""Flask entry point for the Tinshed Roster web application.

Run with: python -m flask --app src.app run
"""

from pathlib import Path

from flask import Flask

from src.views import views_bp

# Templates live in the project-root templates/ directory (see README).
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
    app.register_blueprint(views_bp)
    return app


app = create_app()
