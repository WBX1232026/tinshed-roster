"""Tests for the volunteer personal view (feature/volunteer-personal-view)."""

from datetime import date

import pytest

from src.assignment import AssignmentStore
from src.performance import PerformanceStore
from src.personal import NotFoundError, PersonalView
from src.production import ProductionStore
from src.volunteer import VolunteerStore


@pytest.fixture
def view():
    volunteers = VolunteerStore()
    volunteers.create("Col Hendricks")
    volunteers.create("Kylie Toomey")
    productions = ProductionStore()
    productions.create("The Weather House")
    performances = PerformanceStore(productions)
    performances.create(1, "2026-09-04", "19:30")  # id 1
    performances.create(1, "2026-09-05", "14:00")  # id 2
    assignments = AssignmentStore(volunteers, performances)
    return (
        PersonalView(volunteers, assignments, performances, productions),
        volunteers,
        performances,
        assignments,
    )


def test_assignments_for_returns_own_assignments_with_show_details(view):
    personal, _, performances, assignments = view
    assignments.create(1, 1, "Bar")
    assignments.create(2, 1, "Front of House")

    results = personal.assignments_for(1)

    assert len(results) == 2
    first = results[0]
    assert first.role == "Bar"
    assert first.performance_date == date(2026, 9, 4)
    assert first.start_time == "19:30"
    assert first.production_title == "The Weather House"


def test_assignments_are_sorted_by_performance_date_then_time(view):
    personal, _, performances, assignments = view
    assignments.create(2, 1, "Front of House")  # later performance first
    assignments.create(1, 1, "Bar")

    results = personal.assignments_for(1)

    assert [r.role for r in results] == ["Bar", "Front of House"]


def test_other_volunteers_assignments_are_not_included(view):
    personal, _, performances, assignments = view
    assignments.create(1, 1, "Bar")
    assignments.create(1, 2, "Front of House")

    results = personal.assignments_for(1)

    assert len(results) == 1
    assert results[0].role == "Bar"


def test_volunteer_without_assignments_gets_empty_list(view):
    personal, _, performances, assignments = view

    assert personal.assignments_for(2) == []


def test_unknown_volunteer_raises(view):
    personal, _, performances, assignments = view

    with pytest.raises(NotFoundError):
        personal.assignments_for(999)
