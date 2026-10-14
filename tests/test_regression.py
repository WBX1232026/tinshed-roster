"""Regression smoke tests covering every story area.

Run after any change to catch regressions across the whole application.
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


def test_regression_volunteer_create_and_find():
    v = models.create_volunteer("Aisha Bello", "0400 000 111", "aisha@example.com")
    assert models.find_volunteer(v.id).name == "Aisha Bello"


def test_regression_blank_volunteer_name_rejected():
    with pytest.raises(ValueError):
        models.create_volunteer("   ")


def test_regression_production_and_performances_ordered():
    p = models.create_production("The Weather House")
    perf1 = models.create_performance(p.id, "2026-09-04", "19:30")
    perf2 = models.create_performance(p.id, "2026-09-05", "14:00")
    assert [x.id for x in models.performances_for_production(p.id)] == [
        perf1.id,
        perf2.id,
    ]


def test_regression_crew_call_defined():
    p = models.create_production("The Weather House")
    perf = models.create_performance(p.id, "2026-09-04", "19:30")
    models.set_crew_call(perf.id, "Usher", 2)
    assert models.crew_call_for(perf.id) == {"Usher": 2}


def test_regression_one_role_rule_holds():
    p = models.create_production("The Weather House")
    perf = models.create_performance(p.id, "2026-09-04", "19:30")
    v = models.create_volunteer("Sam O'Connor", "0400 555 666")
    models.create_assignment(perf.id, "Bar 1", v.id)
    with pytest.raises(ValueError, match="already assigned"):
        models.create_assignment(perf.id, "Sound Op", v.id)


def test_regression_roster_gap_open_positions():
    p = models.create_production("The Weather House")
    perf = models.create_performance(p.id, "2026-09-04", "19:30")
    models.set_crew_call(perf.id, "Usher", 2)
    v = models.create_volunteer("Grace Kim", "0400 888 999")
    models.create_assignment(perf.id, "Usher", v.id)
    assert models.roster_gaps(perf.id) == [
        {"role": "Usher", "needed": 2, "assigned": 1, "open": 1}
    ]


def test_regression_personal_view_lists_own_assignments():
    p = models.create_production("The Weather House")
    perf = models.create_performance(p.id, "2026-09-04", "19:30")
    v1 = models.create_volunteer("Tom Nguyen", "0400 777 888")
    v2 = models.create_volunteer("Elena Rossi", "0400 666 777")
    models.create_assignment(perf.id, "Bar 1", v1.id)
    assert [a.volunteer_id for a in models.assignments_for_volunteer(v1.id)] == [v1.id]
    assert models.assignments_for_volunteer(v2.id) == []
