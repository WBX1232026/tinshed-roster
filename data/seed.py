"""Load the sample CSVs in data/ into the module-level models.

Run with: python data/seed.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

# Make the project root importable when run as `python data/seed.py`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import models

DATA_DIR = Path(__file__).resolve().parent


def load_seed_data() -> None:
    """Load data/sample_volunteers.csv and data/sample_productions.csv."""
    with open(
        DATA_DIR / "sample_volunteers.csv", newline="", encoding="utf-8"
    ) as handle:
        for row in csv.DictReader(handle):
            volunteer = models.create_volunteer(
                row["name"], phone=row.get("phone", ""), email=row.get("email", "")
            )
            if row.get("active", "true").strip().lower() != "true":
                volunteer.active = False

    production_ids: dict[str, int] = {}
    with open(
        DATA_DIR / "sample_productions.csv", newline="", encoding="utf-8"
    ) as handle:
        for row in csv.DictReader(handle):
            title = row["production_title"]
            if title not in production_ids:
                production_ids[title] = models.create_production(title).id
            models.create_performance(
                production_ids[title], row["performance_date"], row["start_time"]
            )


if __name__ == "__main__":
    load_seed_data()
    print(
        f"Seeded {len(models.volunteers)} volunteers and "
        f"{len(models.productions)} productions "
        f"({len(models.performances)} performances)."
    )
