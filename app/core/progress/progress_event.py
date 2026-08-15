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
from datetime import datetime
from typing import Any

from app.core.progress.progress_stage import ProgressStage

__all__ = [
    "ProgressEvent",
]


@dataclass(slots=True, frozen=True)
class ProgressEvent:
    """
    Immutable progress event emitted during workflow execution.

    Parameters
    ----------
    stage
        Current workflow stage.

    message
        Human-readable progress message.

    percentage
        Completion percentage (0-100).

    timestamp
        Event creation timestamp.

    metadata
        Optional provider-specific information.
    """

    stage: ProgressStage

    message: str

    percentage: int

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )