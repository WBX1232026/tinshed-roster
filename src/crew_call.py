"""Crew call management for the Tinshed Roster.

Feature branch: feature/crew-call-define
Story: As a coordinator, I want to define which roles are needed for each
performance and how many people each role needs, so the roster can be
checked against the real crew call.
"""

from __future__ import annotations

from src.errors import NotFoundError, ValidationError
from src.performance import PerformanceStore

__all__ = ["ValidationError", "NotFoundError", "CrewCallStore"]


class CrewCallStore:
    """In-memory store of crew-call requirements per performance.

    A crew call maps a role name (e.g. "Front of House") to the number of
    volunteers needed for that role in one performance.
    """

    def __init__(self, performances: PerformanceStore) -> None:
        self._performances = performances
        self._calls: dict[int, dict[str, int]] = {}

    def set_requirement(self, performance_id: int, role: str, needed: int) -> None:
        """Set (or update) how many volunteers a role needs for a performance.

        Raises NotFoundError if the performance does not exist and
        ValidationError if the role is blank or needed < 1.
        """
        self._performances.find(performance_id)
        role = (role or "").strip()
        if not role:
            raise ValidationError("Role name is required.")
        if not isinstance(needed, int) or isinstance(needed, bool) or needed < 1:
            raise ValidationError("Number needed must be a positive whole number.")
        self._calls.setdefault(performance_id, {})[role] = needed

    def remove_role(self, performance_id: int, role: str) -> None:
        """Remove a role from a performance's crew call (no-op if absent)."""
        self._performances.find(performance_id)
        calls = self._calls.get(performance_id)
        if calls:
            calls.pop((role or "").strip(), None)

    def requirements_for(self, performance_id: int) -> dict[str, int]:
        """Return {role: number needed} for one performance (empty if none).

        Raises NotFoundError if the performance does not exist.
        """
        self._performances.find(performance_id)
        return dict(self._calls.get(performance_id, {}))

    def total_needed(self, performance_id: int) -> int:
        """Return the total number of volunteers needed for a performance."""
        return sum(self.requirements_for(performance_id).values())

    def all_requirements(self) -> dict[int, dict[str, int]]:
        """Return {performance_id: {role: needed}} for every performance."""
        return {pid: dict(roles) for pid, roles in self._calls.items()}

    def restore(self, calls: dict[int, dict[str, int]]) -> None:
        """Replace the store contents (used by the persistence layer)."""
        self._calls = {pid: dict(roles) for pid, roles in calls.items()}
