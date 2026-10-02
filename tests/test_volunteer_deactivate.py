"""Tests for volunteer deactivation (feature/volunteer-deactivate)."""

import pytest

from src.volunteer import NotFoundError, VolunteerStore


@pytest.fixture
def store():
    s = VolunteerStore()
    s.create("Col Hendricks")
    s.create("Kylie Toomey")
    return s


def test_deactivate_marks_volunteer_inactive(store):
    volunteer = store.deactivate(1)

    assert volunteer.active is False


def test_deactivated_volunteer_leaves_other_records_untouched(store):
    store.deactivate(1)

    assert store.find(1).active is False
    assert store.find(2).active is True


def test_deactivated_volunteer_is_excluded_from_find_all_by_default(store):
    store.deactivate(1)

    names = [v.name for v in store.find_all()]

    assert names == ["Kylie Toomey"]


def test_deactivated_volunteer_appears_when_active_only_false(store):
    store.deactivate(1)

    names = [v.name for v in store.find_all(active_only=False)]

    assert names == ["Col Hendricks", "Kylie Toomey"]


def test_deactivate_unknown_volunteer_raises(store):
    with pytest.raises(NotFoundError):
        store.deactivate(999)


def test_deactivate_is_idempotent(store):
    store.deactivate(1)
    store.deactivate(1)

    assert store.find(1).active is False
