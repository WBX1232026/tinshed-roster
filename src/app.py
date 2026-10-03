"""Flask entry point for the Tinshed Roster web application.

Run with: python -m flask --app src.app run
"""

import os
from pathlib import Path

from flask import Flask

from src.views import views_bp

# Templates live in the project-root templates/ directory (see README).
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"


def _bootstrap_data() -> None:
    """Load persisted data, or seed the sample season, at startup.

    DATABASE_URL and SEED_DATA come from the environment (see .env.example).
    """
    from src import database, models

    db_url = os.environ.get("DATABASE_URL", "sqlite:///data/tinshed_roster.db")
    db_path = Path(db_url.replace("sqlite:///", ""))
    if db_path.exists():
        database.load(db_path)
        return
    if os.environ.get("SEED_DATA", "true").strip().lower() == "true":
        from data.seed import load_seed_data

        load_seed_data()


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
    _bootstrap_data()
    app.register_blueprint(views_bp)
    return app


app = create_app()
