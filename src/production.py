"""Production management for the Tinshed Roster.

Feature branch: feature/production-create
Story: As a coordinator, I want to create productions so that performances
can be scheduled under them.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.errors import NotFoundError, ValidationError

__all__ = ["ValidationError", "NotFoundError", "Production", "ProductionStore"]


@dataclass
class Production:
    """A theatre production, e.g. "The Weather House"."""

    title: str
    id: int | None = None


class ProductionStore:
    """In-memory store for productions."""

    def __init__(self) -> None:
        self._productions: dict[int, Production] = {}
        self._next_id = 1

    def create(self, title: str) -> Production:
        """Create a production and return the stored record."""
        title = (title or "").strip()
        if not title:
            raise ValidationError("Production title is required.")
        production = Production(title=title, id=self._next_id)
        self._next_id += 1
        self._productions[production.id] = production
        return production

    def find(self, production_id: int) -> Production:
        """Return the production with the given id."""
        try:
            return self._productions[production_id]
        except KeyError:
            raise NotFoundError(f"No production with id {production_id}.") from None

    def find_all(self) -> list[Production]:
        """Return all productions in creation order."""
        return list(self._productions.values())

    def restore(self, productions: list[Production]) -> None:
        """Replace the store contents (used by the persistence layer)."""
        self._productions = {p.id: p for p in productions}
        self._next_id = max((p.id for p in productions), default=0) + 1
