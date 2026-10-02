"""Tests for performance creation (feature/performance-create)."""

from datetime import date

import pytest

from src.performance import NotFoundError, PerformanceStore, ValidationError
from src.production import ProductionStore


@pytest.fixture
def productions():
    store = ProductionStore()
    store.create("The Weather House")
    return store


@pytest.fixture
def performances(productions):
    return PerformanceStore(productions)


def test_create_performance_with_iso_date_string(performances):
    performance = performances.create(1, "2026-09-04", "19:30")

    assert performance.production_id == 1
    assert performance.performance_date == date(2026, 9, 4)
    assert performance.start_time == "19:30"
    assert performance.id == 1


def test_create_accepts_date_object(performances):
    performance = performances.create(1, date(2026, 9, 5), "14:00")

    assert performance.performance_date == date(2026, 9, 5)


def test_create_rejects_unknown_production(performances):
    with pytest.raises(NotFoundError):
        performances.create(999, "2026-09-04", "19:30")


def test_create_rejects_invalid_date(performances):
    with pytest.raises(ValidationError):
        performances.create(1, "04-09-2026", "19:30")
    with pytest.raises(ValidationError):
        performances.create(1, "not-a-date", "19:30")


def test_create_rejects_invalid_time(performances):
    with pytest.raises(ValidationError):
        performances.create(1, "2026-09-04", "7:30pm")
    with pytest.raises(ValidationError):
        performances.create(1, "2026-09-04", "25:00")
    with pytest.raises(ValidationError):
        performances.create(1, "2026-09-04", "")


def test_find_unknown_performance_raises(performances):
    with pytest.raises(NotFoundError):
        performances.find(999)
