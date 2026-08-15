"""
===============================================================================
Project      : AI Research Assistant
Module       : Generic Pipeline Framework
File         : diagnostic_message.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines structured diagnostic messages used during pipeline execution.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

__all__ = [
    "DiagnosticLevel",
    "DiagnosticMessage",
]


class DiagnosticLevel(Enum):
    """Severity level for diagnostic messages."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DiagnosticMessage:
    """
    Represents a single diagnostic event.
    """

    level: DiagnosticLevel
    message: str
    step: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)