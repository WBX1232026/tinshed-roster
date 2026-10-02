"""Tests for performance listing (feature/performance-list)."""

from datetime import date

import pytest

from src.performance import NotFoundError, PerformanceStore
from src.production import ProductionStore


@pytest.fixture
def productions():
    store = ProductionStore()
    store.create("The Weather House")
    store.create("The 39 Steps")
    return store


@pytest.fixture
def performances(productions):
    store = PerformanceStore(productions)
    # deliberately created out of chronological order
    store.create(1, "2026-09-12", "19:30")
    store.create(1, "2026-09-04", "19:30")
    store.create(2, "2026-10-02", "19:30")
    store.create(1, "2026-09-05", "14:00")
    store.create(1, "2026-09-05", "19:30")
    return store


def test_list_for_production_returns_only_that_production(performances):
    results = performances.list_for_production(1)

    assert len(results) == 4
    assert all(p.production_id == 1 for p in results)


def test_list_for_production_sorts_by_date_then_time(performances):
    results = performances.list_for_production(1)

    assert [
        (p.performance_date, p.start_time)
        for p in results
    ] == [
        (date(2026, 9, 4), "19:30"),
        (date(2026, 9, 5), "14:00"),
        (date(2026, 9, 5), "19:30"),
        (date(2026, 9, 12), "19:30"),
    ]


def test_list_for_unknown_production_raises(performances):
    with pytest.raises(NotFoundError):
        performances.list_for_production(999)


def test_list_for_production_returns_only_that_productions_shows(performances):
    results = performances.list_for_production(2)

    assert len(results) == 1
    assert results[0].performance_date == date(2026, 10, 2)
