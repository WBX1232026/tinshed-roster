"""Acceptance tests for the three core UAT scenarios.

Mirrors docs/uat.md:
  A. Build a full roster for a performance.
  B. One-role rule.
  C. Personal roster view.
"""

import pytest
from src import models


def setup_function():
    models.volunteers.clear()
    models.productions.clear()
    models.performances.clear()
    models.crew_calls.clear()
    models.assignments.clear()
    models._next_volunteer_id = 1
    models._next_production_id = 1
    models._next_performance_id = 1
    models._next_assignment_id = 1


def _show_with_call():
    prod = models.create_production("The Weather House")
    perf = models.create_performance(prod.id, "2026-09-04", "19:30")
    models.set_crew_call(perf.id, "Bar 1", 1)
    models.set_crew_call(perf.id, "Sound Op", 1)
    models.set_crew_call(perf.id, "Usher", 2)
    return prod, perf


def test_acceptance_scenario_a_build_full_roster():
    _, perf = _show_with_call()
    col = models.create_volunteer("Col Hendricks", "0400 111 222", "col@example.com")
    wendy = models.create_volunteer("Wendy Tran", "0400 222 333", "wendy@example.com")

    a_col = models.create_assignment(perf.id, "Bar 1", col.id)
    models.create_assignment(perf.id, "Sound Op", wendy.id)

    # New assignments default to "unconfirmed", then can be confirmed.
    assert a_col.status == "unconfirmed"
    models.confirm_assignment(a_col.id)
    assert models.assignments[a_col.id].status == "confirmed"

    # Roster gap view: filled roles show open == 0, the Usher role is open.
    gaps = {g["role"]: g for g in models.roster_gaps(perf.id)}
    assert gaps["Bar 1"]["open"] == 0
    assert gaps["Sound Op"]["open"] == 0
    assert gaps["Usher"]["open"] == 2


def test_acceptance_scenario_b_one_role_rule():
    _, perf = _show_with_call()
    col = models.create_volunteer("Col Hendricks", "0400 111 222", "col@example.com")
    models.create_assignment(perf.id, "Sound Op", col.id)

    with pytest.raises(ValueError, match="already assigned"):
        models.create_assignment(perf.id, "Bar 1", col.id)


def test_acceptance_scenario_c_personal_roster_view():
    _, perf = _show_with_call()
    col = models.create_volunteer("Col Hendricks", "0400 111 222", "col@example.com")
    wendy = models.create_volunteer("Wendy Tran", "0400 222 333", "wendy@example.com")
    models.create_assignment(perf.id, "Bar 1", wendy.id)

    mine = models.assignments_for_volunteer(wendy.id)
    assert [a.role for a in mine] == ["Bar 1"]

    # A volunteer with no assignments gets an empty list, not an error.
    assert models.assignments_for_volunteer(col.id) == []
