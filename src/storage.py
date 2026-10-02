"""Persistence and seed data for the Tinshed Roster.

Feature branch: feature/persistence-seed-data
Stories: sample data is seeded from data/*.csv, and the whole roster can be
snapshotted to / restored from a SQLite database.
"""

from __future__ import annotations

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

from src.assignment import Assignment, AssignmentStore
from src.crew_call import CrewCallStore
from src.performance import Performance, PerformanceStore
from src.production import Production, ProductionStore
from src.volunteer import Volunteer, VolunteerStore

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS volunteers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL DEFAULT '',
    email TEXT NOT NULL DEFAULT '',
    active INTEGER NOT NULL,
    created_at TEXT
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


def load_seed_data(
    volunteers: VolunteerStore,
    productions: ProductionStore,
    performances: PerformanceStore,
) -> None:
    """Load the sample CSVs from data/ into the given (empty) stores."""
    with open(
        DATA_DIR / "sample_volunteers.csv", newline="", encoding="utf-8"
    ) as handle:
        for row in csv.DictReader(handle):
            volunteer = volunteers.create(
                row["name"], phone=row.get("phone", ""), email=row.get("email", "")
            )
            if row.get("active", "true").strip().lower() != "true":
                volunteers.deactivate(volunteer.id)

    production_ids: dict[str, int] = {}
    with open(
        DATA_DIR / "sample_productions.csv", newline="", encoding="utf-8"
    ) as handle:
        for row in csv.DictReader(handle):
            title = row["production_title"]
            if title not in production_ids:
                production_ids[title] = productions.create(title).id
            performances.create(
                production_ids[title], row["performance_date"], row["start_time"]
            )


def save_snapshot(
    db_path: str | Path,
    volunteers: VolunteerStore,
    productions: ProductionStore,
    performances: PerformanceStore,
    crew_calls: CrewCallStore,
    assignments: AssignmentStore,
) -> None:
    """Write every store into a SQLite database (replacing previous contents)."""
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(_SCHEMA)
        for table in ("assignments", "crew_calls", "performances", "productions", "volunteers"):
            connection.execute(f"DELETE FROM {table}")

        for volunteer in volunteers.find_all(active_only=False):
            connection.execute(
                "INSERT INTO volunteers (id, name, phone, email, active, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    volunteer.id,
                    volunteer.name,
                    volunteer.phone,
                    volunteer.email,
                    int(volunteer.active),
                    volunteer.created_at.isoformat() if volunteer.created_at else None,
                ),
            )
        for production in productions.find_all():
            connection.execute(
                "INSERT INTO productions (id, title) VALUES (?, ?)",
                (production.id, production.title),
            )
        for performance in performances.find_all():
            connection.execute(
                "INSERT INTO performances (id, production_id, performance_date, start_time) "
                "VALUES (?, ?, ?, ?)",
                (
                    performance.id,
                    performance.production_id,
                    performance.performance_date.isoformat(),
                    performance.start_time,
                ),
            )
        for performance_id, roles in crew_calls.all_requirements().items():
            for role, needed in roles.items():
                connection.execute(
                    "INSERT INTO crew_calls (performance_id, role, needed) VALUES (?, ?, ?)",
                    (performance_id, role, needed),
                )
        for assignment in assignments.find_all():
            connection.execute(
                "INSERT INTO assignments (id, performance_id, volunteer_id, role, status) "
                "VALUES (?, ?, ?, ?, ?)",
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


def load_snapshot(
    db_path: str | Path,
    volunteers: VolunteerStore,
    productions: ProductionStore,
    performances: PerformanceStore,
    crew_calls: CrewCallStore,
    assignments: AssignmentStore,
) -> None:
    """Restore all stores from a snapshot. No-op if the file does not exist."""
    db_path = Path(db_path)
    if not db_path.exists():
        return
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(_SCHEMA)
        productions.restore(
            [
                Production(id=row[0], title=row[1])
                for row in connection.execute("SELECT id, title FROM productions")
            ]
        )
        performances.restore(
            [
                Performance(
                    id=row[0],
                    production_id=row[1],
                    performance_date=datetime.strptime(row[2], "%Y-%m-%d").date(),
                    start_time=row[3],
                )
                for row in connection.execute(
                    "SELECT id, production_id, performance_date, start_time "
                    "FROM performances"
                )
            ]
        )
        volunteers.restore(
            [
                Volunteer(
                    id=row[0],
                    name=row[1],
                    phone=row[2],
                    email=row[3],
                    active=bool(row[4]),
                    created_at=(
                        datetime.fromisoformat(row[5]) if row[5] else None
                    ),
                )
                for row in connection.execute(
                    "SELECT id, name, phone, email, active, created_at FROM volunteers"
                )
            ]
        )
        calls: dict[int, dict[str, int]] = {}
        for performance_id, role, needed in connection.execute(
            "SELECT performance_id, role, needed FROM crew_calls"
        ):
            calls.setdefault(performance_id, {})[role] = needed
        crew_calls.restore(calls)
        assignments.restore(
            [
                Assignment(
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
            ]
        )
    finally:
        connection.close()
