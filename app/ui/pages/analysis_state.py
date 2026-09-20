"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Page
File         : analysis_state.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Analysis page lifecycle states.
===============================================================================
"""

from enum import StrEnum


__all__ = [
    "AnalysisState",
]


class AnalysisState(StrEnum):
    """
    Analysis page lifecycle.
    """

    IDLE = "idle"

    PREVIEW = "preview"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"