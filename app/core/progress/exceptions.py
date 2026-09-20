"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress
File         : exceptions.py
Version      : 1.0.0

Description:
    Exceptions used by the progress and cancellation framework.
===============================================================================
"""

from __future__ import annotations

__all__ = [
    "AnalysisCancelledError",
]


class AnalysisCancelledError(Exception):
    """
    Raised when the user cancels an analysis workflow.
    """

    def __init__(
        self,
        message: str = "Analysis cancelled by user.",
    ) -> None:
        super().__init__(message)