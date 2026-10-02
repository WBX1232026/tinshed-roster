"""Shared exceptions for the Tinshed Roster domain.

Kept in one module so every store raises the same error types; modules
re-export them for convenience (e.g. `from src.volunteer import ValidationError`
keeps working).
"""


class ValidationError(ValueError):
    """Raised when a record fails validation."""


class NotFoundError(LookupError):
    """Raised when a record cannot be found."""


class RuleViolationError(ValueError):
    """Raised when a domain rule (e.g. the one-role rule) would be broken."""
