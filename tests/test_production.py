"""Tests for production creation (feature/production-create)."""

import pytest

from src.production import NotFoundError, ProductionStore, ValidationError


@pytest.fixture
def store():
    return ProductionStore()


def test_create_production_stores_title(store):
    production = store.create("The Weather House")

    assert production.title == "The Weather House"
    assert production.id == 1


def test_create_assigns_unique_sequential_ids(store):
    first = store.create("The Weather House")
    second = store.create("The 39 Steps")

    assert first.id == 1
    assert second.id == 2


def test_create_trims_whitespace(store):
    production = store.create("  The Weather House  ")

    assert production.title == "The Weather House"


def test_create_rejects_blank_title(store):
    with pytest.raises(ValidationError):
        store.create("")
    with pytest.raises(ValidationError):
        store.create("   ")


def test_find_returns_created_production(store):
    production = store.create("The Weather House")

    assert store.find(production.id).title == "The Weather House"


def test_find_unknown_id_raises(store):
    with pytest.raises(NotFoundError):
        store.find(999)
