"""Configuration validation errors."""

from __future__ import annotations


class ConfigurationError(ValueError):
    """Raised when application configuration is invalid."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)
