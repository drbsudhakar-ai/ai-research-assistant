"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Lifecycle
File         : analysis_state.py
Version      : 4.0.0
Author       : Dr. B. Sudhakar

Description:
    Runtime state model for a research paper analysis.

Purpose:
    Centralize all analysis lifecycle data into a single strongly-typed object.

Benefits:
    - Single source of truth.
    - Eliminates scattered Streamlit session keys.
    - Rerun-safe.
    - Thread-safe (controller owns updates).
    - Supports cancellation.
    - Supports multi-agent execution.
    - Supports future provider switching.
===============================================================================
"""

from __future__ import annotations

from app.core.progress.progress_state import ProgressState
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from threading import Thread
from typing import Any

from app.core.analysis.analysis_status import AnalysisStatus


@dataclass(slots=True)
class AnalysisState:
    """
    Runtime state of a single analysis execution.

    This object contains all mutable state required by the
    analysis controller.

    It replaces numerous Streamlit session variables with one
    strongly typed model.
    """

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    status: AnalysisStatus = AnalysisStatus.IDLE

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------

    created_at: datetime = field(default_factory=datetime.now)

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # ------------------------------------------------------------------
    # Progress
    # ------------------------------------------------------------------

    progress: int = 0

    message: str = ""

    # ------------------------------------------------------------------
    # Background execution
    # ------------------------------------------------------------------

    worker: Thread | None = None

    # ------------------------------------------------------------------
    # Analysis data
    # ------------------------------------------------------------------

    uploaded_file: Any | None = None

    prepared_paper: Any | None = None

    # ------------------------------------------------------------------
    # PDF Preview
    # ------------------------------------------------------------------

    pdf_bytes: bytes | None = None


    # Extracted paper sections
    # Example:
    # {
    #     "abstract": "...",
    #     "introduction": "...",
    #     "methodology": "...",
    #     "results": "...",
    #     "discussion": "...",
    #     "conclusion": "..."
    # }
    sections: dict[str, Any] = field(default_factory=dict)

    analysis_result: Any | None = None

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    error: Exception | None = None

    error_message: str = ""

    # ------------------------------------------------------------------
    # Cancellation
    # ------------------------------------------------------------------

    cancelled: bool = False

    # ------------------------------------------------------------------
    # Worker communication
    # ------------------------------------------------------------------

    result_holder: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def is_idle(self) -> bool:
        return self.status == AnalysisStatus.IDLE

    @property
    def is_running(self) -> bool:
        return self.status.is_active

    @property
    def is_completed(self) -> bool:
        return self.status == AnalysisStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.status == AnalysisStatus.FAILED

    @property
    def is_cancelled(self) -> bool:
        return self.status == AnalysisStatus.CANCELLED

    @property
    def has_result(self) -> bool:
        return self.analysis_result is not None

    @property
    def has_error(self) -> bool:
        return self.error is not None

    @property
    def duration_seconds(self) -> float:
        """
        Returns total execution time in seconds.

        While running, returns elapsed time.

        When finished, returns total duration.
        """

        if self.started_at is None:
            return 0.0

        end = self.finished_at or datetime.now()

        return (end - self.started_at).total_seconds()

    # ------------------------------------------------------------------
    # Lifecycle Methods
    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Mark analysis as started.
        """

        self.status = AnalysisStatus.RUNNING

        self.started_at = datetime.now()

        self.finished_at = None

        self.progress = 0

        self.message = ""

        self.error = None

        self.error_message = ""

        self.cancelled = False

        self.analysis_result = None

    def complete(self, result: Any) -> None:
        """
        Mark analysis as successfully completed.
        """

        self.status = AnalysisStatus.COMPLETED

        self.finished_at = datetime.now()

        self.progress = 100

        self.analysis_result = result

    def fail(
        self,
        error: Exception,
    ) -> None:
        """
        Mark analysis as failed.
        """

        self.status = AnalysisStatus.FAILED

        self.finished_at = datetime.now()

        self.error = error

        self.error_message = str(error)

    def cancel(self) -> None:
        """
        Mark analysis as cancelled.
        """

        self.status = AnalysisStatus.CANCELLED

        self.finished_at = datetime.now()

        self.cancelled = True

    def reset(self) -> None:
        """
        Reset the analysis state.

        Called before starting a new analysis.
        """

        self.status = AnalysisStatus.IDLE

        self.started_at = None

        self.finished_at = None

        self.progress = 0

        self.message = ""

        self.worker = None

        self.analysis_result = None

        self.sections.clear()

        self.error = None

        self.error_message = ""

        self.cancelled = False

        self.result_holder.clear()

    # ------------------------------------------------------------------
    # Progress lifecycle
    # ------------------------------------------------------------------

    progress_state: ProgressState = field(
        default_factory=ProgressState
    )