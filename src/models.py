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
crew_calls: dict[int, dict[str, int]] = {}
assignments: dict[int, "Assignment"] = {}

_next_volunteer_id = 1
_next_production_id = 1
_next_performance_id = 1
_next_assignment_id = 1

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


@dataclass
class Assignment:
    """One volunteer filling one role at one performance."""

    id: int
    performance_id: int
    volunteer_id: int
    role: str
    status: str = "unconfirmed"


def set_crew_call(performance_id: int, role: str, needed: int) -> None:
    """Set (or update) how many volunteers a role needs for a performance."""
    if performance_id not in performances:
        raise ValueError(f"No performance with id {performance_id}.")
    role = (role or "").strip()
    if not role:
        raise ValueError("Role name is required.")
    if not isinstance(needed, int) or needed < 1:
        raise ValueError("Number needed must be a positive whole number.")
    crew_calls.setdefault(performance_id, {})[role] = needed


def crew_call_for(performance_id: int) -> dict[str, int]:
    """Return {role: needed} for one performance (empty if none defined)."""
    return dict(crew_calls.get(performance_id, {}))


def create_assignment(performance_id: int, role: str, volunteer_id: int) -> Assignment:
    """Assign a volunteer to a role at a performance.

    Enforces the one-role rule: a volunteer may hold at most one role in the
    same performance. Raises ValueError if the volunteer is already assigned
    to this performance.
    """
    global _next_assignment_id
    if performance_id not in performances:
        raise ValueError(f"No performance with id {performance_id}.")
    volunteer = find_volunteer(volunteer_id)
    if not volunteer.active:
        raise ValueError(
            f"Volunteer {volunteer_id} is inactive and cannot be assigned."
        )
    role = (role or "").strip()
    if not role:
        raise ValueError("Role is required.")

    # One-role rule
    for existing in assignments.values():
        if (
            existing.performance_id == performance_id
            and existing.volunteer_id == volunteer_id
        ):
            raise ValueError(
                f"Volunteer {volunteer_id} is already assigned to role "
                f"{existing.role!r} in performance {performance_id}."
            )

    assignment = Assignment(
        id=_next_assignment_id,
        performance_id=performance_id,
        volunteer_id=volunteer_id,
        role=role,
    )
    assignments[assignment.id] = assignment
    _next_assignment_id += 1
    return assignment


def confirm_assignment(assignment_id: int) -> Assignment:
    """Mark an assignment as confirmed."""
    try:
        assignment = assignments[assignment_id]
    except KeyError:
        raise ValueError(f"No assignment with id {assignment_id}.") from None
    assignment.status = "confirmed"
    return assignment


def assignments_for_performance(performance_id: int) -> list[Assignment]:
    """Return all assignments for one performance."""
    return [
        a for a in assignments.values() if a.performance_id == performance_id
    ]


def assignments_for_volunteer(volunteer_id: int) -> list[Assignment]:
    """Return all assignments for one volunteer."""
    return [
        a for a in assignments.values() if a.volunteer_id == volunteer_id
    ]


def roster_gaps(performance_id: int) -> list[dict]:
    """Compare the crew call with the assignments and return the gaps.

    Each entry: {role, needed, assigned, open}. Open never goes negative.
    """
    requirements = crew_call_for(performance_id)
    assigned_counts: dict[str, int] = {}
    for assignment in assignments_for_performance(performance_id):
        if assignment.role in requirements:
            assigned_counts[assignment.role] = (
                assigned_counts.get(assignment.role, 0) + 1
            )
    gaps = []
    for role, needed in requirements.items():
        assigned = assigned_counts.get(role, 0)
        gaps.append(
            {
                "role": role,
                "needed": needed,
                "assigned": assigned,
                "open": max(needed - assigned, 0),
            }
        )
    return gaps
