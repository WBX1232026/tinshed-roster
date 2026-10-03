"""In-memory data models used by the Flask web application.

Module-level API: the Flask views import this module and call the
create_* / set_* functions. Data lives in module-level dicts so tests can
reset the store with .clear() and by resetting the _next_* counters.

Branch: feature/flask-web-app
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime

volunteers: dict[int, "Volunteer"] = {}
productions: dict[int, "Production"] = {}
performances: dict[int, "Performance"] = {}

_next_volunteer_id = 1
_next_production_id = 1
_next_performance_id = 1

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


@dataclass
class Volunteer:
    """A volunteer crew member."""

    id: int
    name: str
    phone: str = ""
    email: str = ""
    active: bool = True


@dataclass
class Production:
    """A theatre production, e.g. "The Weather House"."""

    id: int
    title: str


@dataclass
class Performance:
    """One performance of a production with a date and a start time."""

    id: int
    production_id: int
    performance_date: date
    start_time: str


def create_volunteer(name: str, phone: str = "", email: str = "") -> Volunteer:
    """Create an active volunteer; blank names are rejected."""
    global _next_volunteer_id
    name = (name or "").strip()
    if not name:
        raise ValueError("Volunteer name is required.")
    volunteer = Volunteer(
        id=_next_volunteer_id,
        name=name,
        phone=(phone or "").strip(),
        email=(email or "").strip(),
    )
    volunteers[volunteer.id] = volunteer
    _next_volunteer_id += 1
    return volunteer


def find_volunteer(volunteer_id: int) -> Volunteer:
    """Return the volunteer with the given id."""
    try:
        return volunteers[volunteer_id]
    except KeyError:
        raise ValueError(f"No volunteer with id {volunteer_id}.") from None


def create_production(title: str) -> Production:
    """Create a production; blank titles are rejected."""
    global _next_production_id
    title = (title or "").strip()
    if not title:
        raise ValueError("Production title is required.")
    production = Production(id=_next_production_id, title=title)
    productions[production.id] = production
    _next_production_id += 1
    return production


def create_performance(
    production_id: int, performance_date: str, start_time: str
) -> Performance:
    """Create a performance for an existing production.

    performance_date must be "YYYY-MM-DD"; start_time must be "HH:MM".
    """
    global _next_performance_id
    if production_id not in productions:
        raise ValueError(f"No production with id {production_id}.")
    try:
        parsed_date = datetime.strptime(performance_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            f"Performance date must be YYYY-MM-DD, got {performance_date!r}."
        ) from None
    if not _TIME_RE.match(start_time):
        raise ValueError(
            f"Start time must be HH:MM (24-hour), got {start_time!r}."
        )
    performance = Performance(
        id=_next_performance_id,
        production_id=production_id,
        performance_date=parsed_date,
        start_time=start_time,
    )
    performances[performance.id] = performance
    _next_performance_id += 1
    return performance


def performances_for_production(production_id: int) -> list[Performance]:
    """Return a production's performances sorted by date, then time."""
    return sorted(
        (p for p in performances.values() if p.production_id == production_id),
        key=lambda p: (p.performance_date, p.start_time),
    )
