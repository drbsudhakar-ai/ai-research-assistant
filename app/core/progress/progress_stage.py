"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Framework
File         : progress_stage.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines workflow stages for long-running operations.
===============================================================================
"""

from __future__ import annotations

from enum import Enum, auto

__all__ = ["ProgressStage"]


class ProgressStage(Enum):
    """Workflow stages."""

    STARTING = auto()

    VALIDATING = auto()

    EXTRACTING_TEXT = auto()

    EXTRACTING_TITLE = auto()

    PREPROCESSING = auto()

    BUILDING_CONTEXT = auto()

    ANALYZING = auto()

    SAVING = auto()

    COMPLETED = auto()

    FAILED = auto()

    CANCELLED = auto()