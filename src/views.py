"""Flask routes (views) for the Tinshed Roster web application."""

from flask import Blueprint, render_template

from src import models

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    production_list = []
    for production in sorted(
        models.productions.values(), key=lambda p: p.title
    ):
        production_list.append(
            {
                "id": production.id,
                "title": production.title,
                "performance_count": len(
                    models.performances_for_production(production.id)
                ),
            }
        )
    return render_template("index.html", productions=production_list)


@views_bp.route("/productions")
def productions():
    """All productions (same view as the index; kept for the nav link)."""
    return index()


@views_bp.route("/volunteers")
def volunteers():
    volunteer_list = sorted(
        models.volunteers.values(), key=lambda v: v.name
    )
    return render_template("volunteers.html", volunteers=volunteer_list)


@views_bp.route("/productions/<int:production_id>")
def production_detail(production_id: int):
    production = models.productions.get(production_id)
    if production is None:
        return "Production not found", 404
    performance_list = []
    for performance in models.performances_for_production(production_id):
        performance_list.append(
            {
                "id": performance.id,
                "performance_date": performance.performance_date.isoformat(),
                "start_time": performance.start_time,
                "gaps": models.roster_gaps(performance.id),
            }
        )
    return render_template(
        "productions.html",
        production=production,
        performances=performance_list,
    )


@views_bp.route("/volunteers/<int:volunteer_id>")
def personal(volunteer_id: int):
    """A volunteer's own assignments across the season."""
    volunteer = models.volunteers.get(volunteer_id)
    if volunteer is None:
        return "Volunteer not found", 404
    assignment_list = []
    for assignment in models.assignments_for_volunteer(volunteer_id):
        performance = models.performances.get(assignment.performance_id)
        production = models.productions.get(performance.production_id)
        assignment_list.append(
            {
                "role": assignment.role,
                "status": assignment.status,
                "production_title": production.title,
                "performance_date": performance.performance_date.isoformat(),
                "start_time": performance.start_time,
            }
        )
    assignment_list.sort(
        key=lambda a: (a["performance_date"], a["start_time"], a["role"])
    )
    return render_template(
        "personal.html",
        volunteer=volunteer,
        assignments=assignment_list,
    )


@views_bp.route("/performances/<int:performance_id>/roster")
def roster(performance_id: int):
    """Roster for one performance: roles, how many are filled and open, and who is on."""
    performance = models.performances.get(performance_id)
    if performance is None:
        return "Performance not found", 404
    production = models.productions.get(performance.production_id)
    assigned_names: dict[str, list[str]] = {}
    for assignment in models.assignments_for_performance(performance_id):
        assigned_names.setdefault(assignment.role, []).append(
            models.find_volunteer(assignment.volunteer_id).name
        )
    rows = []
    for gap in models.roster_gaps(performance_id):
        rows.append(
            {
                "role": gap["role"],
                "needed": gap["needed"],
                "assigned": gap["assigned"],
                "open": gap["open"],
                "names": sorted(assigned_names.get(gap["role"], [])),
            }
        )
    return render_template(
        "roster.html",
        production=production,
        performance={
            "performance_date": performance.performance_date.isoformat(),
            "start_time": performance.start_time,
        },
        rows=rows,
    )
