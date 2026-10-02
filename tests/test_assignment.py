"""Tests for assignment creation (feature/assignment-create)."""

import pytest

from src.assignment import AssignmentStore, NotFoundError, UNCONFIRMED
from src.performance import PerformanceStore
from src.production import ProductionStore
from src.volunteer import ValidationError, VolunteerStore


@pytest.fixture
def volunteers():
    store = VolunteerStore()
    store.create("Col Hendricks")
    store.create("Kylie Toomey")
    store.deactivate(2)  # Kylie is inactive
    store.create("Steve Lindquist")
    return store


@pytest.fixture
def performances():
    productions = ProductionStore()
    productions.create("The Weather House")
    store = PerformanceStore(productions)
    store.create(1, "2026-09-04", "19:30")
    store.create(1, "2026-09-05", "14:00")
    return store


@pytest.fixture
def assignments(volunteers, performances):
    return AssignmentStore(volunteers, performances)


def test_create_assignment_defaults_to_unconfirmed(assignments):
    assignment = assignments.create(1, 1, "Front of House")

    assert assignment.status == UNCONFIRMED
    assert assignment.performance_id == 1
    assert assignment.volunteer_id == 1
    assert assignment.role == "Front of House"
    assert assignment.id == 1


def test_create_assigns_unique_sequential_ids(assignments):
    first = assignments.create(1, 1, "Bar")
    second = assignments.create(1, 3, "Front of House")

    assert first.id == 1
    assert second.id == 2


def test_create_rejects_unknown_performance(assignments):
    with pytest.raises(NotFoundError):
        assignments.create(999, 1, "Bar")


def test_create_rejects_unknown_volunteer(assignments):
    with pytest.raises(NotFoundError):
        assignments.create(1, 999, "Bar")


def test_create_rejects_inactive_volunteer(assignments):
    with pytest.raises(ValidationError):
        assignments.create(1, 2, "Bar")


def test_create_rejects_blank_role(assignments):
    with pytest.raises(ValidationError):
        assignments.create(1, 1, "   ")


def test_for_performance_returns_only_that_performance(assignments):
    assignments.create(1, 1, "Bar")
    assignments.create(2, 3, "Bar")

    results = assignments.for_performance(1)

    assert len(results) == 1
    assert results[0].volunteer_id == 1


def test_find_unknown_assignment_raises(assignments):
    with pytest.raises(NotFoundError):
        assignments.find(999)
