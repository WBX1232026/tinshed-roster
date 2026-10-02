"""Personal views for the Tinshed Roster.

Feature branch: feature/volunteer-personal-view
Story: As a volunteer, I want to see my own assignments across the season,
so I know what I have been put down for without asking anyone.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.assignment import AssignmentStore
from src.errors import NotFoundError
from src.performance import PerformanceStore
from src.production import ProductionStore
from src.volunteer import VolunteerStore

__all__ = ["NotFoundError", "VolunteerAssignment", "PersonalView"]


@dataclass
class VolunteerAssignment:
    """One of a volunteer's assignments, enriched with show details."""

    assignment_id: int
    role: str
    status: str
    performance_id: int
    performance_date: date
    start_time: str
    production_title: str


class PersonalView:
    """Read-only views for a single volunteer."""

    def __init__(
        self,
        volunteers: VolunteerStore,
        assignments: AssignmentStore,
        performances: PerformanceStore,
        productions: ProductionStore,
    ) -> None:
        self._volunteers = volunteers
        self._assignments = assignments
        self._performances = performances
        self._productions = productions

    def assignments_for(self, volunteer_id: int) -> list[VolunteerAssignment]:
        """Return the volunteer's assignments, sorted by performance date/time.

        Raises NotFoundError if the volunteer does not exist.
        """
        self._volunteers.find(volunteer_id)
        mine = [
            a
            for a in self._assignments.find_all()
            if a.volunteer_id == volunteer_id
        ]
        enriched = [self._enrich(a) for a in mine]
        return sorted(
            enriched,
            key=lambda v: (v.performance_date, v.start_time, v.role),
        )

    def _enrich(self, assignment) -> VolunteerAssignment:
        performance = self._performances.find(assignment.performance_id)
        production = self._productions.find(performance.production_id)
        return VolunteerAssignment(
            assignment_id=assignment.id,
            role=assignment.role,
            status=assignment.status,
            performance_id=assignment.performance_id,
            performance_date=performance.performance_date,
            start_time=performance.start_time,
            production_title=production.title,
        )
