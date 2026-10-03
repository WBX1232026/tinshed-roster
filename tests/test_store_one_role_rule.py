"""Tests for the one-role rule (feature/one-role-rule).

A volunteer may hold at most one role in the same performance.
"""

import pytest

from src.assignment import AssignmentStore, RuleViolationError
from src.performance import PerformanceStore
from src.production import ProductionStore
from src.volunteer import VolunteerStore


@pytest.fixture
def stores():
    volunteers = VolunteerStore()
    volunteers.create("Col Hendricks")
    volunteers.create("Kylie Toomey")
    productions = ProductionStore()
    productions.create("The Weather House")
    performances = PerformanceStore(productions)
    performances.create(1, "2026-09-04", "19:30")  # Friday evening
    performances.create(1, "2026-09-05", "14:00")  # Saturday matinee
    assignments = AssignmentStore(volunteers, performances)
    return volunteers, performances, assignments


def test_volunteer_cannot_hold_two_roles_in_the_same_performance(stores):
    _, _, assignments = stores

    assignments.create(1, 1, "Bar")
    with pytest.raises(RuleViolationError):
        assignments.create(1, 1, "Front of House")


def test_same_role_twice_is_also_rejected(stores):
    _, _, assignments = stores

    assignments.create(1, 1, "Bar")
    with pytest.raises(RuleViolationError):
        assignments.create(1, 1, "Bar")


def test_volunteer_can_be_assigned_to_different_performances(stores):
    _, _, assignments = stores

    assignments.create(1, 1, "Bar")
    second = assignments.create(2, 1, "Front of House")

    assert second.performance_id == 2


def test_two_volunteers_can_share_a_performance(stores):
    _, _, assignments = stores

    assignments.create(1, 1, "Bar")
    second = assignments.create(1, 2, "Front of House")

    assert second.volunteer_id == 2


def test_rule_violation_mentions_the_conflict(stores):
    _, _, assignments = stores

    assignments.create(1, 1, "Bar")
    with pytest.raises(RuleViolationError, match="Bar"):
        assignments.create(1, 1, "Front of House")


def test_rejected_assignment_is_not_stored(stores):
    _, _, assignments = stores

    assignments.create(1, 1, "Bar")
    with pytest.raises(RuleViolationError):
        assignments.create(1, 1, "Front of House")

    assert len(assignments.find_all()) == 1
