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
