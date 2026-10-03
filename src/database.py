"""SQLite persistence for the module-level models.

`save` writes every model dict into a single SQLite database; `load`
restores them and resets the id counters so new records never collide.

Branch: feature/persistence
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from src import models

_SCHEMA = """
CREATE TABLE IF NOT EXISTS volunteers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL DEFAULT '',
    email TEXT NOT NULL DEFAULT '',
    active INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS productions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS performances (
    id INTEGER PRIMARY KEY,
    production_id INTEGER NOT NULL,
    performance_date TEXT NOT NULL,
    start_time TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS crew_calls (
    performance_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    needed INTEGER NOT NULL,
    PRIMARY KEY (performance_id, role)
);
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY,
    performance_id INTEGER NOT NULL,
    volunteer_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL
);
"""


def save(db_path: str | Path) -> None:
    """Write all models into a SQLite database, replacing previous contents."""
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(_SCHEMA)
        for table in (
            "assignments",
            "crew_calls",
            "performances",
            "productions",
            "volunteers",
        ):
            connection.execute(f"DELETE FROM {table}")

        for volunteer in models.volunteers.values():
            connection.execute(
                "INSERT INTO volunteers (id, name, phone, email, active) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    volunteer.id,
                    volunteer.name,
                    volunteer.phone,
                    volunteer.email,
                    int(volunteer.active),
                ),
            )
        for production in models.productions.values():
            connection.execute(
                "INSERT INTO productions (id, title) VALUES (?, ?)",
                (production.id, production.title),
            )
        for performance in models.performances.values():
            connection.execute(
                "INSERT INTO performances (id, production_id, performance_date, "
                "start_time) VALUES (?, ?, ?, ?)",
                (
                    performance.id,
                    performance.production_id,
                    performance.performance_date.isoformat(),
                    performance.start_time,
                ),
            )
        for performance_id, roles in models.crew_calls.items():
            for role, needed in roles.items():
                connection.execute(
                    "INSERT INTO crew_calls (performance_id, role, needed) "
                    "VALUES (?, ?, ?)",
                    (performance_id, role, needed),
                )
        for assignment in models.assignments.values():
            connection.execute(
                "INSERT INTO assignments (id, performance_id, volunteer_id, "
                "role, status) VALUES (?, ?, ?, ?, ?)",
                (
                    assignment.id,
                    assignment.performance_id,
                    assignment.volunteer_id,
                    assignment.role,
                    assignment.status,
                ),
            )
        connection.commit()
    finally:
        connection.close()


def load(db_path: str | Path) -> None:
    """Restore all models from a SQLite database. No-op if missing."""
    db_path = Path(db_path)
    if not db_path.exists():
        return
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(_SCHEMA)
        models.productions = {
            row[0]: models.Production(id=row[0], title=row[1])
            for row in connection.execute("SELECT id, title FROM productions")
        }
        models.performances = {
            row[0]: models.Performance(
                id=row[0],
                production_id=row[1],
                performance_date=datetime.strptime(row[2], "%Y-%m-%d").date(),
                start_time=row[3],
            )
            for row in connection.execute(
                "SELECT id, production_id, performance_date, start_time "
                "FROM performances"
            )
        }
        models.volunteers = {
            row[0]: models.Volunteer(
                id=row[0],
                name=row[1],
                phone=row[2],
                email=row[3],
                active=bool(row[4]),
            )
            for row in connection.execute(
                "SELECT id, name, phone, email, active FROM volunteers"
            )
        }
        models.crew_calls = {}
        for performance_id, role, needed in connection.execute(
            "SELECT performance_id, role, needed FROM crew_calls"
        ):
            models.crew_calls.setdefault(performance_id, {})[role] = needed
        models.assignments = {
            row[0]: models.Assignment(
                id=row[0],
                performance_id=row[1],
                volunteer_id=row[2],
                role=row[3],
                status=row[4],
            )
            for row in connection.execute(
                "SELECT id, performance_id, volunteer_id, role, status "
                "FROM assignments"
            )
        }
    finally:
        connection.close()

    # Reset id counters so new records never collide with restored ids.
    models._next_volunteer_id = (
        max(models.volunteers, default=0) + 1
    )
    models._next_production_id = (
        max(models.productions, default=0) + 1
    )
    models._next_performance_id = (
        max(models.performances, default=0) + 1
    )
    models._next_assignment_id = (
        max(models.assignments, default=0) + 1
    )
