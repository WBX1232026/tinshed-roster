"""Performance management for the Tinshed Roster.

Feature branch: feature/performance-create
Story: As a coordinator, I want to create performances with a date and start
time so that the season calendar exists in the system.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime

from src.errors import NotFoundError, ValidationError
from src.production import ProductionStore

__all__ = [
    "ValidationError",
    "NotFoundError",
    "Performance",
    "PerformanceStore",
]

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


@dataclass
class Performance:
    """One performance of a production, e.g. Friday 2026-09-04 at 19:30."""

    production_id: int
    performance_date: date
    start_time: str  # "HH:MM" (24-hour)
    id: int | None = None


class PerformanceStore:
    """In-memory store for performances. Requires a ProductionStore."""

    def __init__(self, productions: ProductionStore) -> None:
        self._productions = productions
        self._performances: dict[int, Performance] = {}
        self._next_id = 1

    def create(
        self, production_id: int, performance_date: str | date, start_time: str
    ) -> Performance:
        """Create a performance for an existing production.

        performance_date is an ISO date string "YYYY-MM-DD" or a date object;
        start_time must look like "HH:MM" (24-hour).
        """
        self._productions.find(production_id)  # raises NotFoundError

        if isinstance(performance_date, str):
            try:
                parsed_date = datetime.strptime(
                    (performance_date or "").strip(), "%Y-%m-%d"
                ).date()
            except ValueError:
                raise ValidationError(
                    "Performance date must be YYYY-MM-DD, "
                    f"got {performance_date!r}."
                ) from None
        elif isinstance(performance_date, date):
            parsed_date = performance_date
        else:
            raise ValidationError(
                "Performance date must be a YYYY-MM-DD string or a date."
            )

        start_time = (start_time or "").strip()
        if not _TIME_RE.match(start_time):
            raise ValidationError(
                f"Start time must be HH:MM (24-hour), got {start_time!r}."
            )

        performance = Performance(
            production_id=production_id,
            performance_date=parsed_date,
            start_time=start_time,
            id=self._next_id,
        )
        self._next_id += 1
        self._performances[performance.id] = performance
        return performance

    def find(self, performance_id: int) -> Performance:
        """Return the performance with the given id."""
        try:
            return self._performances[performance_id]
        except KeyError:
            raise NotFoundError(
                f"No performance with id {performance_id}."
            ) from None

    def find_all(self) -> list[Performance]:
        """Return all performances sorted by date, then start time."""
        return sorted(
            self._performances.values(),
            key=lambda p: (p.performance_date, p.start_time),
        )

    def list_for_production(self, production_id: int) -> list[Performance]:
        """Return the performances of one production, sorted by date then time.

        Raises NotFoundError if the production does not exist.
        """
        self._productions.find(production_id)
        return [
            p
            for p in self.find_all()
            if p.production_id == production_id
        ]

    def restore(self, performances: list[Performance]) -> None:
        """Replace the store contents (used by the persistence layer)."""
        self._performances = {p.id: p for p in performances}
        self._next_id = max((p.id for p in performances), default=0) + 1
