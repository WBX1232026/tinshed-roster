"""Tests for crew call viewing (feature/crew-call-view)."""

import pytest

from src.crew_call import CrewCallStore
from src.performance import NotFoundError, PerformanceStore
from src.production import ProductionStore


@pytest.fixture
def calls():
    productions = ProductionStore()
    productions.create("The Weather House")
    performances = PerformanceStore(productions)
    performances.create(1, "2026-09-04", "19:30")
    performances.create(1, "2026-09-05", "14:00")
    store = CrewCallStore(performances)
    store.set_requirement(1, "Front of House", 2)
    store.set_requirement(1, "Bar", 1)
    store.set_requirement(1, "Stage Manager", 1)
    store.set_requirement(2, "Bar", 3)
    return store


def test_requirements_for_returns_all_roles(calls):
    assert calls.requirements_for(1) == {
        "Front of House": 2,
        "Bar": 1,
        "Stage Manager": 1,
    }


def test_total_needed_sums_all_roles(calls):
    assert calls.total_needed(1) == 4
    assert calls.total_needed(2) == 3


def test_requirements_for_returns_copy(calls):
    requirements = calls.requirements_for(1)
    requirements["Front of House"] = 99

    assert calls.requirements_for(1)["Front of House"] == 2  # unchanged


def test_requirements_for_unknown_performance_raises(calls):
    with pytest.raises(NotFoundError):
        calls.requirements_for(999)
