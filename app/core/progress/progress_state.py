"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Framework
File         : progress_state.py
Version      : 2.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


from app.core.progress.progress_stage import ProgressStage

__all__ = ["ProgressState"]


@dataclass(slots=True)
class ProgressState:
    """
    Mutable workflow progress state.
    """

    stage: ProgressStage = ProgressStage.STARTING

    percentage: int = 0

    status: str = "Waiting..."

    elapsed_seconds: float = 0.0

    completed: bool = False

    cancelled: bool = False

    failed: bool = False

    error_message: str | None = None
    
    metadata: dict[str, Any] = field(default_factory=dict)

    def reset(self) -> None:
        """Reset workflow state."""

        self.stage = ProgressStage.STARTING

        self.percentage = 0

        self.status = "Waiting..."

        self.elapsed_seconds = 0.0

        self.completed = False

        self.cancelled = False

        self.failed = False

        self.error_message = None