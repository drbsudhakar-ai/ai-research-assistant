"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Reporter
File         : progress_reporter.py
Version      : 2.0.0

Description:
    Reporting abstraction used by pipeline steps to publish progress updates.

    Pipeline code should never directly communicate with Streamlit.
    All progress communication goes through this component.

===============================================================================
"""

from __future__ import annotations

from typing import Any, Protocol
from app.core.progress.progress_stage import ProgressStage


__all__ = [
    "ProgressReporter",
]



class ProgressReporter(Protocol):
    """
    Protocol for progress reporting.

    Any progress implementation can satisfy this interface.
    """


    def update(
        self,
        message: str,
        percentage: float | None = None,
        stage: ProgressStage | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Publish a progress update.

        Parameters
        ----------
        message:
            Human readable progress message.

        percentage:
            Completion percentage (0-100).

        stage:
            Current ProgressStage.

        metadata:
            Additional information.
        """

        ...