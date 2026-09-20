"""Domain and application contract errors.

These are independent of Streamlit, SQLite, and LLM SDKs.
Pipeline framework errors remain in ``app.core.pipeline.exceptions``.
Configuration errors remain in ``app.config.exceptions``.
"""

from __future__ import annotations


class DomainError(Exception):
    """Base class for domain-contract failures."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)


class DomainValidationError(DomainError, ValueError):
    """Raised when a domain contract is structurally invalid."""


class DocumentError(DomainError):
    """Raised when paper/document data cannot be used for analysis."""


class AnalysisError(DomainError):
    """Raised when analysis production fails for domain reasons."""


class PersistenceError(DomainError):
    """Raised when a history/persistence contract is invalid.

    SQLite-specific failures belong in the repository layer.
    """
