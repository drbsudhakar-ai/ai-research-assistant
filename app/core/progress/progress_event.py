"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Framework
File         : progress_event.py
Version      : 3.0.0
Author       : Dr. B. Sudhakar

Description:
    Represents a single workflow progress event.

Responsibilities:
    - Encapsulate progress information.
    - Remain independent of UI.
    - Support future streaming providers.

Notes:
    - Immutable.
    - No Streamlit dependencies.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from app.core.progress.progress_stage import ProgressStage
from app.models.exceptions import DomainValidationError

__all__ = [
    "ProgressEvent",
]


@dataclass(slots=True, frozen=True)
class ProgressEvent:
    """Immutable, UI-independent progress event."""

    stage: ProgressStage
    message: str
    percentage: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.stage, ProgressStage):
            raise DomainValidationError(
                "stage must be a ProgressStage.",
                field="stage",
            )
        if not 0 <= int(self.percentage) <= 100:
            raise DomainValidationError(
                "percentage must be between 0 and 100.",
                field="percentage",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage.name,
            "message": self.message,
            "percentage": self.percentage,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }
