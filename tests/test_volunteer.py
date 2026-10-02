"""Tests for volunteer creation (feature/volunteer-create)."""

import pytest

from src.volunteer import NotFoundError, ValidationError, VolunteerStore


@pytest.fixture
def store():
    return VolunteerStore()


def test_create_volunteer_stores_an_active_record(store):
    volunteer = store.create(
        "Kylie Toomey", phone="0409 226 731", email="kylie@example.com"
    )

    assert volunteer.name == "Kylie Toomey"
    assert volunteer.phone == "0409 226 731"
    assert volunteer.email == "kylie@example.com"
    assert volunteer.active is True


def test_create_assigns_unique_sequential_ids(store):
    first = store.create("Col Hendricks")
    second = store.create("Steve Lindquist")

    assert first.id == 1
    assert second.id == 2
    assert first.id != second.id


def test_created_volunteer_can_be_found(store):
    volunteer = store.create("Vera Sokolova")

    found = store.find(volunteer.id)

    assert found.name == "Vera Sokolova"
    assert found.id == volunteer.id


def test_create_rejects_blank_name(store):
    with pytest.raises(ValidationError):
        store.create("")
    with pytest.raises(ValidationError):
        store.create("   ")


def test_create_trims_whitespace_around_name(store):
    volunteer = store.create("  Marion D'Souza  ")

    assert volunteer.name == "Marion D'Souza"


def test_find_unknown_id_raises(store):
    with pytest.raises(NotFoundError):
        store.find(999)
