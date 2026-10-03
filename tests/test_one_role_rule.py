"""One-role rule tests against the module-level models API.

A volunteer may hold at most one role in the same performance.
"""

import pytest
from src import models


def setup_function():
    models.volunteers.clear()
    models.performances.clear()
    models.assignments.clear()
    models.productions.clear()
    models.crew_calls.clear()
    models._next_volunteer_id = 1
    models._next_production_id = 1
    models._next_performance_id = 1
    models._next_assignment_id = 1


def test_volunteer_cannot_hold_two_roles_in_same_performance():
    v = models.create_volunteer("Col Hendricks", "0400 111 222", "col@example.com")
    prod = models.create_production("The Weather House")
    perf = models.create_performance(prod.id, "2026-09-04", "19:30")
    models.create_assignment(perf.id, "Bar 1", v.id)
    with pytest.raises(ValueError, match="already assigned"):
        models.create_assignment(perf.id, "Sound Op", v.id)


def test_volunteer_can_hold_roles_in_different_performances():
    v = models.create_volunteer("Col Hendricks", "0400 111 222", "col@example.com")
    prod = models.create_production("The Weather House")
    p1 = models.create_performance(prod.id, "2026-09-04", "19:30")
    p2 = models.create_performance(prod.id, "2026-09-05", "14:00")
    models.create_assignment(p1.id, "Bar 1", v.id)
    models.create_assignment(p2.id, "Bar 1", v.id)
    assert len(models.assignments) == 2


def test_moving_assignment_respects_one_role_rule():
    v = models.create_volunteer("Col Hendricks", "0400 111 222", "col@example.com")
    prod = models.create_production("The Weather House")
    p1 = models.create_performance(prod.id, "2026-09-04", "19:30")
    p2 = models.create_performance(prod.id, "2026-09-05", "14:00")
    models.create_assignment(p1.id, "Bar 1", v.id)
    models.create_assignment(p2.id, "Sound Op", v.id)
    with pytest.raises(ValueError, match="already assigned"):
        models.create_assignment(p2.id, "Bar 1", v.id)
