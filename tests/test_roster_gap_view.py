"""Tests for the roster gap view (feature/roster-gap-view)."""

import pytest

from src.assignment import AssignmentStore
from src.crew_call import CrewCallStore
from src.performance import NotFoundError, PerformanceStore
from src.production import ProductionStore
from src.roster import RosterService
from src.volunteer import VolunteerStore


@pytest.fixture
def service():
    volunteers = VolunteerStore()
    for name in ("Col Hendricks", "Steve Lindquist", "Kylie Toomey", "Ade Okoro"):
        volunteers.create(name)
    productions = ProductionStore()
    productions.create("The Weather House")
    performances = PerformanceStore(productions)
    performances.create(1, "2026-09-04", "19:30")
    performances.create(1, "2026-09-05", "14:00")
    crew_calls = CrewCallStore(performances)
    crew_calls.set_requirement(1, "Front of House", 2)
    crew_calls.set_requirement(1, "Bar", 1)
    assignments = AssignmentStore(volunteers, performances)
    return RosterService(assignments, crew_calls), assignments


def test_empty_roster_shows_all_positions_open(service):
    roster, _ = service

    gaps = roster.gaps_for(1)

    assert [(g.role, g.needed, g.assigned, g.open) for g in gaps] == [
        ("Front of House", 2, 0, 2),
        ("Bar", 1, 0, 1),
    ]


def test_partially_filled_role_shows_remaining_open(service):
    roster, assignments = service
    assignments.create(1, 1, "Front of House")

    gaps = roster.gaps_for(1)

    foh = next(g for g in gaps if g.role == "Front of House")
    assert (foh.assigned, foh.open) == (1, 1)
    bar = next(g for g in gaps if g.role == "Bar")
    assert (bar.assigned, bar.open) == (0, 1)


def test_fully_filled_role_shows_no_open(service):
    roster, assignments = service
    assignments.create(1, 1, "Front of House")
    assignments.create(1, 2, "Front of House")

    gaps = roster.gaps_for(1)

    foh = next(g for g in gaps if g.role == "Front of House")
    assert (foh.assigned, foh.open) == (2, 0)


def test_overfilled_role_never_shows_negative_open(service):
    roster, assignments = service
    assignments.create(1, 1, "Bar")
    assignments.create(1, 2, "Bar")  # overfills Bar (needs 1)

    gaps = roster.gaps_for(1)

    bar = next(g for g in gaps if g.role == "Bar")
    assert (bar.assigned, bar.open) == (2, 0)


def test_assignments_outside_the_crew_call_do_not_add_rows(service):
    roster, assignments = service
    assignments.create(1, 1, "Some Other Role")

    gaps = roster.gaps_for(1)

    assert [g.role for g in gaps] == ["Front of House", "Bar"]


def test_gaps_for_unknown_performance_raises(service):
    roster, _ = service

    with pytest.raises(NotFoundError):
        roster.gaps_for(999)


def test_performance_without_crew_call_has_no_gaps(service):
    roster, _ = service

    assert roster.gaps_for(2) == []
