"""
===============================================================================
Project      : AI Research Assistant
Module       : Bootstrap
File         : analysis_controller.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Central controller responsible for coordinating the paper analysis
    lifecycle.

Responsibilities:
    - Own the analysis lifecycle.
    - Manage analysis-related session state.
    - Delegate execution to AnalysisService.
    - Provide a clean API for the UI layer.

Non-Responsibilities:
    - UI rendering.
    - Progress rendering.
    - Pipeline construction.
    - Business logic.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.core.session import (
    get_session_value,
    set_session_value,
)
from app.models.analysis_request import AnalysisRequest
from app.services.analysis_service import AnalysisService

__all__ = [
    "AnalysisController",
]


class AnalysisController:
    """
    Controller responsible for coordinating research paper analysis.

    The controller owns the analysis lifecycle while delegating execution
    to AnalysisService.
    """

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(
        self,
        analysis_service: AnalysisService,
    ) -> None:

        if analysis_service is None:
            raise ValueError(
                "analysis_service cannot be None."
            )

        self._analysis_service = analysis_service

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def analysis_service(self) -> AnalysisService:
        """
        Return configured analysis service.
        """

        return self._analysis_service

    @property
    def is_running(self) -> bool:
        """
        Return whether analysis is currently running.
        """

        return bool(
            get_session_value(
                "analysis_running",
            )
        )

    @property
    def is_completed(self) -> bool:
        """
        Return whether analysis completed successfully.
        """

        return bool(
            get_session_value(
                "analysis_completed",
            )
        )

    @property
    def has_failed(self) -> bool:
        """
        Return whether analysis failed.
        """

        return bool(
            get_session_value(
                "analysis_failed",
            )
        )

    @property
    def result(self) -> Any:
        """
        Return analysis result.
        """

        return get_session_value(
            "analysis_result",
        )

    @property
    def error(self) -> Any:
        """
        Return analysis error.
        """

        return get_session_value(
            "analysis_error",
        )

    # =========================================================================
    # Lifecycle
    # =========================================================================

    def start(
        self,
        request: AnalysisRequest,
    ) -> None:
        """
        Prepare analysis lifecycle.

        Actual pipeline execution will be introduced in Part 2.
        """

        if request is None:
            raise ValueError(
                "request cannot be None."
            )

        self.reset()

        set_session_value(
            "analysis_running",
            True,
        )

    def cancel(self) -> None:
        """
        Cancel the current analysis.

        Actual cancellation logic will be implemented in Part 2.
        """

        set_session_value(
            "analysis_running",
            False,
        )

    def complete(
        self,
        result: Any,
    ) -> None:
        """
        Mark analysis as completed.
        """

        set_session_value(
            "analysis_running",
            False,
        )

        set_session_value(
            "analysis_completed",
            True,
        )

        set_session_value(
            "analysis_result",
            result,
        )

    def fail(
        self,
        error: Exception,
    ) -> None:
        """
        Mark analysis as failed.
        """

        set_session_value(
            "analysis_running",
            False,
        )

        set_session_value(
            "analysis_failed",
            True,
        )

        set_session_value(
            "analysis_error",
            error,
        )

    def reset(self) -> None:
        """
        Reset analysis lifecycle state.
        """

        set_session_value(
            "analysis_running",
            False,
        )

        set_session_value(
            "analysis_completed",
            False,
        )

        set_session_value(
            "analysis_failed",
            False,
        )

        set_session_value(
            "analysis_result",
            None,
        )

        set_session_value(
            "analysis_error",
            None,
        )

    # =========================================================================
    # Representation
    # =========================================================================

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"running={self.is_running}, "
            f"completed={self.is_completed}, "
            f"failed={self.has_failed})"
        )