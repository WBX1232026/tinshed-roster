"""Tests for persistence and seed data (feature/persistence-seed-data)."""

from datetime import date

import pytest

from src.assignment import AssignmentStore
from src.crew_call import CrewCallStore
from src.performance import PerformanceStore
from src.production import ProductionStore
from src.storage import load_seed_data, load_snapshot, save_snapshot
from src.volunteer import VolunteerStore


def build_stores():
    volunteers = VolunteerStore()
    productions = ProductionStore()
    performances = PerformanceStore(productions)
    crew_calls = CrewCallStore(performances)
    assignments = AssignmentStore(volunteers, performances)
    return volunteers, productions, performances, crew_calls, assignments


@pytest.fixture
def stores():
    return build_stores()


def test_seed_loads_sample_volunteers(stores):
    volunteers, productions, performances, _, _ = stores

    load_seed_data(volunteers, productions, performances)

    names = [v.name for v in volunteers.find_all()]
    assert len(names) == 10
    assert names[0] == "Col Hendricks"
    assert "Kylie Toomey" in names


def test_seed_loads_production_and_performances(stores):
    volunteers, productions, performances, _, _ = stores

    load_seed_data(volunteers, productions, performances)

    assert len(productions.find_all()) == 1
    production = productions.find_all()[0]
    assert production.title == "The Weather House"
    shows = performances.list_for_production(production.id)
    assert len(shows) == 8
    assert (shows[0].performance_date, shows[0].start_time) == (
        date(2026, 9, 4),
        "19:30",
    )
    assert (shows[-1].performance_date, shows[-1].start_time) == (
        date(2026, 9, 13),
        "14:00",
    )


def test_snapshot_round_trip_preserves_everything(stores, tmp_path):
    volunteers, productions, performances, crew_calls, assignments = stores
    load_seed_data(volunteers, productions, performances)
    crew_calls.set_requirement(1, "Front of House", 2)
    crew_calls.set_requirement(1, "Bar", 1)
    assignments.create(1, 1, "Bar")
    volunteers.deactivate(2)
    db_path = tmp_path / "roster.db"

    save_snapshot(db_path, volunteers, productions, performances, crew_calls, assignments)
    loaded = build_stores()
    load_snapshot(db_path, *loaded)
    lv, lp, lperf, lcalls, lassign = loaded

    assert [v.name for v in lv.find_all(active_only=False)] == [
        v.name for v in volunteers.find_all(active_only=False)
    ]
    assert [v.active for v in lv.find_all(active_only=False)] == [
        v.active for v in volunteers.find_all(active_only=False)
    ]
    assert [p.title for p in lp.find_all()] == [
        p.title for p in productions.find_all()
    ]
    assert [
        (s.performance_date, s.start_time) for s in lperf.find_all()
    ] == [(s.performance_date, s.start_time) for s in performances.find_all()]
    assert lcalls.requirements_for(1) == crew_calls.requirements_for(1)
    assert [
        (a.volunteer_id, a.role, a.status) for a in lassign.find_all()
    ] == [(a.volunteer_id, a.role, a.status) for a in assignments.find_all()]


def test_ids_continue_after_restore(stores, tmp_path):
    volunteers, productions, performances, crew_calls, assignments = stores
    load_seed_data(volunteers, productions, performances)
    db_path = tmp_path / "roster.db"
    save_snapshot(db_path, volunteers, productions, performances, crew_calls, assignments)

    loaded = build_stores()
    lv, lp, _, _, _ = loaded
    load_snapshot(db_path, *loaded)

    new_volunteer = lv.create("New Person")
    assert new_volunteer.id == 11  # 10 seeded volunteers
    new_production = lp.create("Another Show")
    assert new_production.id == 2


def test_load_from_missing_file_is_a_noop(stores):
    volunteers, productions, performances, crew_calls, assignments = stores

    load_snapshot(
        "does/not/exist.db",
        volunteers, productions, performances, crew_calls, assignments,
    )

    assert volunteers.find_all() == []
    assert productions.find_all() == []
