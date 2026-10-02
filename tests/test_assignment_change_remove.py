"""Tests for assignment change and removal (feature/assignment-change-remove)."""

import pytest

from src.assignment import AssignmentStore, CONFIRMED, NotFoundError
from src.performance import PerformanceStore
from src.production import ProductionStore
from src.volunteer import ValidationError, VolunteerStore


@pytest.fixture
def stores():
    volunteers = VolunteerStore()
    volunteers.create("Col Hendricks")
    productions = ProductionStore()
    productions.create("The Weather House")
    performances = PerformanceStore(productions)
    performances.create(1, "2026-09-04", "19:30")
    assignments = AssignmentStore(volunteers, performances)
    return volunteers, performances, assignments


def test_change_role_updates_assignment(stores):
    _, _, assignments = stores
    assignment = assignments.create(1, 1, "Bar")

    changed = assignments.change(assignment.id, role="Front of House")

    assert changed.role == "Front of House"
    assert assignments.find(assignment.id).role == "Front of House"


def test_change_status_to_confirmed(stores):
    _, _, assignments = stores
    assignment = assignments.create(1, 1, "Bar")

    changed = assignments.change(assignment.id, status=CONFIRMED)

    assert changed.status == CONFIRMED


def test_change_rejects_invalid_status(stores):
    _, _, assignments = stores
    assignment = assignments.create(1, 1, "Bar")

    with pytest.raises(ValidationError):
        assignments.change(assignment.id, status="maybe")


def test_change_rejects_blank_role(stores):
    _, _, assignments = stores
    assignment = assignments.create(1, 1, "Bar")

    with pytest.raises(ValidationError):
        assignments.change(assignment.id, role="  ")


def test_change_unknown_assignment_raises(stores):
    _, _, assignments = stores

    with pytest.raises(NotFoundError):
        assignments.change(999, role="Bar")


def test_remove_deletes_assignment(stores):
    _, _, assignments = stores
    assignment = assignments.create(1, 1, "Bar")

    assignments.remove(assignment.id)

    assert assignments.find_all() == []
    with pytest.raises(NotFoundError):
        assignments.find(assignment.id)


def test_remove_unknown_assignment_raises(stores):
    _, _, assignments = stores

    with pytest.raises(NotFoundError):
        assignments.remove(999)


def test_removal_frees_the_volunteer_for_the_performance(stores):
    _, _, assignments = stores
    first = assignments.create(1, 1, "Bar")

    assignments.remove(first.id)
    second = assignments.create(1, 1, "Front of House")

    assert second.role == "Front of House"
