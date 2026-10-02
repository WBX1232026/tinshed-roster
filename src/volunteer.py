"""Volunteer management for the Tinshed Roster.

Feature branch: feature/volunteer-create
Story: As a coordinator, I want to create volunteer records so that they can
be assigned to performances later.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from src.errors import NotFoundError, ValidationError  # noqa: F401  (re-exported)

__all__ = [
    "ValidationError",
    "NotFoundError",
    "Volunteer",
    "VolunteerStore",
]


@dataclass
class Volunteer:
    """A volunteer crew member."""

    name: str
    phone: str = ""
    email: str = ""
    active: bool = True
    id: int | None = None
    created_at: datetime | None = None


class VolunteerStore:
    """In-memory store for volunteers.

    Persistence (SQLite / seed data) arrives in a later story.
    """

    def __init__(self) -> None:
        self._volunteers: dict[int, Volunteer] = {}
        self._next_id = 1

    def create(self, name: str, phone: str = "", email: str = "") -> Volunteer:
        """Create a new active volunteer and return the stored record.

        Raises ValidationError if the name is blank.
        """
        name = (name or "").strip()
        if not name:
            raise ValidationError("Volunteer name is required.")

        volunteer = Volunteer(
            name=name,
            phone=(phone or "").strip(),
            email=(email or "").strip(),
            id=self._next_id,
            created_at=datetime.now(timezone.utc),
        )
        self._next_id += 1
        self._volunteers[volunteer.id] = volunteer
        return volunteer

    def find(self, volunteer_id: int) -> Volunteer:
        """Return the volunteer with the given id."""
        try:
            return self._volunteers[volunteer_id]
        except KeyError:
            raise NotFoundError(f"No volunteer with id {volunteer_id}.") from None

    def find_all(self, active_only: bool = True) -> list[Volunteer]:
        """Return all volunteers in creation order.

        Inactive volunteers are excluded by default; pass active_only=False
        to include them.
        """
        volunteers = list(self._volunteers.values())
        if active_only:
            volunteers = [v for v in volunteers if v.active]
        return volunteers

    def find_by_name(self, name: str) -> list[Volunteer]:
        """Return volunteers whose name contains the given text (case-insensitive)."""
        needle = (name or "").strip().lower()
        if not needle:
            return []
        return [
            v for v in self.find_all(active_only=False) if needle in v.name.lower()
        ]

    def update(
        self,
        volunteer_id: int,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> Volunteer:
        """Update fields of an existing volunteer; None means "leave unchanged"."""
        volunteer = self.find(volunteer_id)
        if name is not None:
            new_name = (name or "").strip()
            if not new_name:
                raise ValidationError("Volunteer name is required.")
            volunteer.name = new_name
        if phone is not None:
            volunteer.phone = (phone or "").strip()
        if email is not None:
            volunteer.email = (email or "").strip()
        return volunteer

    def deactivate(self, volunteer_id: int) -> Volunteer:
        """Mark a volunteer inactive. Existing records and assignments are kept."""
        volunteer = self.find(volunteer_id)
        volunteer.active = False
        return volunteer

    def restore(self, volunteers: list[Volunteer]) -> None:
        """Replace the store contents (used by the persistence layer)."""
        self._volunteers = {v.id: v for v in volunteers}
        self._next_id = max((v.id for v in volunteers), default=0) + 1
