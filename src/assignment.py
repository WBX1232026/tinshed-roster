"""Assignment management for the Tinshed Roster.

Feature branch: feature/assignment-create
Story: As a coordinator, I want to assign a volunteer to a role at a
performance, so the roster starts filling up. New assignments default to
"unconfirmed" until the volunteer confirms.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.errors import NotFoundError, RuleViolationError, ValidationError
from src.performance import PerformanceStore
from src.volunteer import VolunteerStore

__all__ = [
    "ValidationError",
    "NotFoundError",
    "RuleViolationError",
    "Assignment",
    "AssignmentStore",
]

UNCONFIRMED = "unconfirmed"
CONFIRMED = "confirmed"


@dataclass
class Assignment:
    """One volunteer filling one role at one performance."""

    performance_id: int
    volunteer_id: int
    role: str
    status: str = UNCONFIRMED
    id: int | None = None


class AssignmentStore:
    """In-memory store for assignments.

    Requires the volunteer and performance stores so it can check that both
    ends of an assignment exist.
    """

    def __init__(
        self, volunteers: VolunteerStore, performances: PerformanceStore
    ) -> None:
        self._volunteers = volunteers
        self._performances = performances
        self._assignments: dict[int, Assignment] = {}
        self._next_id = 1

    def create(
        self, performance_id: int, volunteer_id: int, role: str
    ) -> Assignment:
        """Assign an active volunteer to a role at a performance.

        New assignments default to "unconfirmed".
        Raises NotFoundError for unknown performances or volunteers,
        ValidationError for blank roles or inactive volunteers.
        (The one-role rule arrives in its own story.)
        """
        self._performances.find(performance_id)
        volunteer = self._volunteers.find(volunteer_id)
        if not volunteer.active:
            raise ValidationError(
                f"Volunteer {volunteer_id} is inactive and cannot be assigned."
            )
        role = (role or "").strip()
        if not role:
            raise ValidationError("Role is required.")

        # One-role rule: a volunteer may hold at most one role in the same
        # performance.
        for existing in self._assignments.values():
            if (
                existing.performance_id == performance_id
                and existing.volunteer_id == volunteer_id
            ):
                raise RuleViolationError(
                    f"Volunteer {volunteer_id} already holds role "
                    f"{existing.role!r} in performance {performance_id}."
                )

        assignment = Assignment(
            performance_id=performance_id,
            volunteer_id=volunteer_id,
            role=role,
            id=self._next_id,
        )
        self._next_id += 1
        self._assignments[assignment.id] = assignment
        return assignment

    def find(self, assignment_id: int) -> Assignment:
        """Return the assignment with the given id."""
        try:
            return self._assignments[assignment_id]
        except KeyError:
            raise NotFoundError(f"No assignment with id {assignment_id}.") from None

    def find_all(self) -> list[Assignment]:
        """Return all assignments in creation order."""
        return list(self._assignments.values())

    def for_performance(self, performance_id: int) -> list[Assignment]:
        """Return all assignments for one performance."""
        self._performances.find(performance_id)
        return [
            a for a in self._assignments.values()
            if a.performance_id == performance_id
        ]

    def change(
        self,
        assignment_id: int,
        role: str | None = None,
        status: str | None = None,
    ) -> Assignment:
        """Change an assignment's role and/or status; None means "unchanged".

        Changing a role cannot break the one-role rule: a volunteer can only
        ever hold this one assignment in the performance.
        """
        assignment = self.find(assignment_id)
        if role is not None:
            new_role = (role or "").strip()
            if not new_role:
                raise ValidationError("Role is required.")
            assignment.role = new_role
        if status is not None:
            if status not in (UNCONFIRMED, CONFIRMED):
                raise ValidationError(
                    f"Status must be {UNCONFIRMED!r} or {CONFIRMED!r}, "
                    f"got {status!r}."
                )
            assignment.status = status
        return assignment

    def remove(self, assignment_id: int) -> None:
        """Delete an assignment (frees the volunteer for that performance)."""
        self.find(assignment_id)
        del self._assignments[assignment_id]

    def restore(self, assignments: list[Assignment]) -> None:
        """Replace the store contents (used by the persistence layer)."""
        self._assignments = {a.id: a for a in assignments}
        self._next_id = max((a.id for a in assignments), default=0) + 1
