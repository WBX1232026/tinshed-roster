"""Tinshed Roster — application entry point.

Run with:
    python src/main.py           seed sample data and show the season
    python src/main.py --demo    full walkthrough of the rostering flow
    python src/main.py --db FILE save the roster to / restore it from SQLite
"""

import sys
from pathlib import Path

# Make the project root importable when run as `python src/main.py`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.assignment import AssignmentStore, CONFIRMED
from src.crew_call import CrewCallStore
from src.errors import RuleViolationError
from src.performance import PerformanceStore
from src.personal import PersonalView
from src.production import ProductionStore
from src.roster import RosterService
from src.storage import load_seed_data, load_snapshot, save_snapshot
from src.volunteer import VolunteerStore


def build_stores(seed: bool = True):
    """Create the five stores, wired together; optionally load sample data."""
    volunteers = VolunteerStore()
    productions = ProductionStore()
    performances = PerformanceStore(productions)
    crew_calls = CrewCallStore(performances)
    assignments = AssignmentStore(volunteers, performances)
    if seed:
        load_seed_data(volunteers, productions, performances)
    return volunteers, productions, performances, crew_calls, assignments


def show_season(stores) -> None:
    volunteers, productions, performances, _, _ = stores
    print(f"Volunteers: {len(volunteers.find_all())} active")
    for production in productions.find_all():
        shows = performances.list_for_production(production.id)
        print(f"\n{production.title} - {len(shows)} performances")
        for show in shows:
            print(f"  {show.performance_date.isoformat()}  {show.start_time}")


def show_demo(stores) -> None:
    _, productions, performances, crew_calls, assignments = stores
    volunteers, _, _, _, _ = stores
    print("== Crew call for the opening night ==")
    opening = performances.list_for_production(productions.find_all()[0].id)[0]
    crew_calls.set_requirement(opening.id, "Front of House", 2)
    crew_calls.set_requirement(opening.id, "Bar", 1)
    crew_calls.set_requirement(opening.id, "Stage Manager", 1)
    for role, needed in crew_calls.requirements_for(opening.id).items():
        print(f"  {role}: {needed}")

    print("\n== Assign volunteers ==")
    bar_volunteer_id = None
    roster = [("Front of House", "Col Hendricks"), ("Front of House", "Steve Lindquist"),
              ("Bar", "Kylie Toomey")]
    for role, name in roster:
        for volunteer in volunteers.find_all():
            if volunteer.name == name:
                assignment = assignments.create(opening.id, volunteer.id, role)
                print(f"  {name} -> {role} [{assignment.status}]")
                if role == "Bar":
                    bar_volunteer_id = volunteer.id

    print("\n== Try to break the one-role rule ==")
    try:
        assignments.create(opening.id, 1, "Bar")
    except RuleViolationError as error:
        print(f"  Rejected: {error}")

    print("\n== Roster gap view for the opening night ==")
    for gap in RosterService(assignments, crew_calls).gaps_for(opening.id):
        flag = "  <-- hole!" if gap.open else ""
        print(
            f"  {gap.role}: need {gap.needed}, "
            f"assigned {gap.assigned}, open {gap.open}{flag}"
        )

    print("\n== Mark one assignment confirmed, show the personal view ==")
    for assignment in assignments.for_performance(opening.id):
        if assignment.role == "Bar":
            assignments.change(assignment.id, status=CONFIRMED)
    personal = PersonalView(
        volunteers, assignments, performances, productions
    )
    for entry in personal.assignments_for(bar_volunteer_id):
        print(
            f"  {entry.production_title} {entry.performance_date} "
            f"{entry.start_time}: {entry.role} [{entry.status}]"
        )


def demo_snapshot(db_path: str, stores) -> None:
    volunteers, productions, performances, crew_calls, assignments = stores
    save_snapshot(db_path, volunteers, productions, performances, crew_calls, assignments)
    print(f"Saved snapshot to {db_path}")

    fresh = build_stores(seed=False)
    load_snapshot(db_path, *fresh)
    loaded_volunteers, loaded_productions, loaded_performances, _, loaded_assignments = fresh
    print(
        f"Reloaded into fresh stores: {len(loaded_volunteers.find_all(active_only=False))} "
        f"volunteers, {len(loaded_productions.find_all())} productions, "
        f"{len(loaded_performances.find_all())} performances, "
        f"{len(loaded_assignments.find_all())} assignments"
    )


def main() -> None:
    print("Tinshed Roster")
    print(
        "Show scheduling and volunteer crew rostering system "
        "for The Tinshed Players Inc."
    )
    if "--db" in sys.argv:
        db_path = sys.argv[sys.argv.index("--db") + 1]
        stores = build_stores()
        demo_snapshot(db_path, stores)
        return

    stores = build_stores()
    if "--demo" in sys.argv:
        show_demo(stores)
    else:
        show_season(stores)


if __name__ == "__main__":
    main()
