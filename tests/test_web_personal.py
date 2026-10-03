"""Web-layer tests for the personal view (feature/volunteer-personal-view)."""

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
    models.create_assignment(1, "Bar", 1)  # Col Hendricks on the bar
    app.testing = True
    return app.test_client()


def test_personal_view_lists_own_assignments(client):
    response = client.get("/volunteers/1")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Col Hendricks" in html
    assert "Bar" in html
    assert "The Weather House" in html


def test_personal_view_excludes_other_volunteers(client):
    response = client.get("/volunteers/2")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "No assignments yet" in html
    assert "Bar" not in html


def test_personal_view_unknown_volunteer_returns_404(client):
    response = client.get("/volunteers/999")

    assert response.status_code == 404
