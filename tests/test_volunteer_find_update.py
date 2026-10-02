"""Tests for volunteer find and update (feature/volunteer-find-update)."""

import pytest

from src.volunteer import NotFoundError, ValidationError, VolunteerStore


@pytest.fixture
def store():
    s = VolunteerStore()
    s.create("Col Hendricks", phone="0400 111 222")
    s.create("Steve Lindquist", phone="0400 333 444")
    s.create("Kylie Toomey", phone="0409 226 731")
    return s


def test_find_all_returns_volunteers_in_creation_order(store):
    names = [v.name for v in store.find_all()]

    assert names == ["Col Hendricks", "Steve Lindquist", "Kylie Toomey"]


def test_find_by_name_matches_case_insensitively(store):
    results = store.find_by_name("kylie")

    assert len(results) == 1
    assert results[0].name == "Kylie Toomey"


def test_find_by_name_supports_partial_match(store):
    results = store.find_by_name("lin")

    assert len(results) == 1
    assert results[0].name == "Steve Lindquist"


def test_find_by_name_blank_returns_empty(store):
    assert store.find_by_name("") == []
    assert store.find_by_name("   ") == []


def test_update_changes_contact_details(store):
    volunteer = store.find(1)

    updated = store.update(1, phone="0499 000 111", email="col@example.com")

    assert updated is volunteer
    assert updated.phone == "0499 000 111"
    assert updated.email == "col@example.com"


def test_update_name_keeps_other_fields(store):
    updated = store.update(2, name="Steven Lindquist")

    assert updated.name == "Steven Lindquist"
    assert updated.phone == "0400 333 444"  # untouched


def test_update_rejects_blank_name(store):
    with pytest.raises(ValidationError):
        store.update(1, name="   ")


def test_update_unknown_volunteer_raises(store):
    with pytest.raises(NotFoundError):
        store.update(999, phone="0400 000 000")
