"""
===============================================================================
Project      : AI Research Assistant
Module       : Document Model
File         : validation_result.py
Version      : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Validation outcome for a processed document.
    """

    valid: bool = True

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    statistics: dict[str, str] = field(default_factory=dict)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)