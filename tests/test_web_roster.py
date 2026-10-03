"""Web-layer tests for the roster view (feature/roster-gap-view)."""

import pytest

from src import models
from src.app import app


def _reset_models():
    models.volunteers.clear()
    models.productions.clear()
    models.performances.clear()
    models.crew_calls.clear()
    models.assignments.clear()
    models._next_volunteer_id = 1
    models._next_production_id = 1
    models._next_performance_id = 1
    models._next_assignment_id = 1


@pytest.fixture
def client():
    _reset_models()
    models.create_production("The Weather House")
    models.create_performance(1, "2026-09-04", "19:30")
    models.create_volunteer("Col Hendricks")
    models.create_volunteer("Kylie Toomey")
    models.set_crew_call(1, "Front of House", 2)
    models.set_crew_call(1, "Bar", 1)
    app.testing = True
    return app.test_client()


def test_roster_view_shows_open_positions_and_assigned_names(client):
    models.create_assignment(1, "Front of House", 1)

    response = client.get("/performances/1/roster")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Front of House" in html
    assert "Col Hendricks" in html
    assert "hole" in html  # the still-open Front of House position is highlighted


def test_roster_view_unknown_performance_returns_404(client):
    response = client.get("/performances/999/roster")

    assert response.status_code == 404
