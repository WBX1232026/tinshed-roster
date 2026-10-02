"""Roster views for the Tinshed Roster.

Feature branch: feature/roster-gap-view
Story: As a coordinator, I want to see, for each performance, which roles are
filled, how many are still open, and where the holes are, so I know what
still needs to be filled.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.assignment import AssignmentStore
from src.crew_call import CrewCallStore
from src.errors import NotFoundError

__all__ = ["NotFoundError", "RoleGap", "RosterService"]


@dataclass
class RoleGap:
    """How one role stands for one performance."""

    role: str
    needed: int
    assigned: int
    open: int


class RosterService:
    """Computes roster views by comparing crew calls with assignments."""

    def __init__(self, assignments: AssignmentStore, crew_calls: CrewCallStore) -> None:
        self._assignments = assignments
        self._crew_calls = crew_calls

    def gaps_for(self, performance_id: int) -> list[RoleGap]:
        """Return one RoleGap per crew-call role for a performance.

        `open` is how many positions are still unfilled. Assignments beyond
        the crew-call number are counted as assigned but never make `open`
        negative.
        """
        requirements = self._crew_calls.requirements_for(performance_id)
        assigned_counts: dict[str, int] = {}
        for assignment in self._assignments.for_performance(performance_id):
            role = assignment.role
            if role in requirements:
                assigned_counts[role] = assigned_counts.get(role, 0) + 1

        gaps = []
        for role, needed in requirements.items():
            assigned = assigned_counts.get(role, 0)
            gaps.append(
                RoleGap(
                    role=role,
                    needed=needed,
                    assigned=assigned,
                    open=max(needed - assigned, 0),
                )
            )
        return gaps
