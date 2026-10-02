"""Tests for crew call definition (feature/crew-call-define)."""

import pytest

from src.crew_call import CrewCallStore
from src.performance import NotFoundError, PerformanceStore
from src.production import ProductionStore, ValidationError


@pytest.fixture
def performances():
    productions = ProductionStore()
    productions.create("The Weather House")
    performances = PerformanceStore(productions)
    performances.create(1, "2026-09-04", "19:30")
    performances.create(1, "2026-09-05", "14:00")
    return performances


@pytest.fixture
def calls(performances):
    return CrewCallStore(performances)


def test_set_requirement_records_role_and_number(calls):
    calls.set_requirement(1, "Front of House", 2)

    assert calls.requirements_for(1) == {"Front of House": 2}


def test_set_requirement_supports_multiple_roles(calls):
    calls.set_requirement(1, "Front of House", 2)
    calls.set_requirement(1, "Bar", 1)
    calls.set_requirement(1, "Stage Manager", 1)

    assert calls.requirements_for(1) == {
        "Front of House": 2,
        "Bar": 1,
        "Stage Manager": 1,
    }


def test_set_requirement_updates_existing_role(calls):
    calls.set_requirement(1, "Bar", 1)
    calls.set_requirement(1, "Bar", 3)

    assert calls.requirements_for(1) == {"Bar": 3}


def test_set_requirement_keeps_calls_separate_per_performance(calls):
    calls.set_requirement(1, "Bar", 2)
    calls.set_requirement(2, "Bar", 1)

    assert calls.requirements_for(1) == {"Bar": 2}
    assert calls.requirements_for(2) == {"Bar": 1}


def test_set_requirement_rejects_unknown_performance(calls):
    with pytest.raises(NotFoundError):
        calls.set_requirement(999, "Bar", 1)


def test_set_requirement_rejects_blank_role(calls):
    with pytest.raises(ValidationError):
        calls.set_requirement(1, "   ", 1)


def test_set_requirement_rejects_non_positive_numbers(calls):
    with pytest.raises(ValidationError):
        calls.set_requirement(1, "Bar", 0)
    with pytest.raises(ValidationError):
        calls.set_requirement(1, "Bar", -2)


def test_remove_role_removes_only_that_role(calls):
    calls.set_requirement(1, "Bar", 1)
    calls.set_requirement(1, "Front of House", 2)

    calls.remove_role(1, "Bar")

    assert calls.requirements_for(1) == {"Front of House": 2}


def test_remove_role_on_unknown_performance_raises(calls):
    with pytest.raises(NotFoundError):
        calls.remove_role(999, "Bar")
