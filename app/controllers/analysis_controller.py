"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Controller
File         : analysis_controller.py
Version      : 4.0.0
Author       : Dr. B. Sudhakar

Description:
    Coordinates the complete lifecycle of a research paper analysis.

Responsibilities:
    - Own AnalysisState
    - Own ProgressManager
    - Own AnalysisWorker
    - Start and monitor background execution
    - Handle completion, failure and cancellation
    - No Streamlit rendering
    - No business logic
===============================================================================
"""

from __future__ import annotations

from threading import Thread
from typing import Any

from app.core.analysis.analysis_state import AnalysisState
from app.core.analysis.analysis_status import AnalysisStatus
from app.core.analysis.analysis_worker import AnalysisWorker
from app.core.progress.progress_manager import ProgressManager
from app.services.analysis_service import AnalysisService


class AnalysisController:
    """
    Coordinates the lifecycle of a paper analysis.

    This controller owns the runtime state but delegates the actual
    analysis to AnalysisWorker and AnalysisService.
    """

    ####################################################################
    # Construction
    ####################################################################

    def __init__(
        self,
        *,
        analysis_service: AnalysisService,
        progress_manager: ProgressManager,
    ) -> None:

        self._analysis_service = analysis_service

        self._progress_manager = progress_manager

        self._worker = AnalysisWorker(
            analysis_service=analysis_service,
        )

        self._state = AnalysisState()

    ####################################################################
    # Public Properties
    ####################################################################

    @property
    def state(self) -> AnalysisState:
        return self._state

    @property
    def progress(self) -> ProgressManager:
        return self._progress_manager

    @property
    def status(self) -> AnalysisStatus:
        return self._state.status

    @property
    def is_running(self) -> bool:
        return self._state.is_running

    @property
    def has_result(self) -> bool:
        return self._state.has_result

    @property
    def has_error(self) -> bool:
        return self._state.has_error

    ####################################################################
    # Preparation
    ####################################################################

    def prepare(
        self,
        *,
        uploaded_file: Any,
        prepared_paper: Any,
    ) -> None:
        """
        Store all inputs required for analysis.
        """

        self._state.uploaded_file = uploaded_file

        self._state.prepared_paper = prepared_paper

    ####################################################################
    # Reset
    ####################################################################

    def reset(self) -> None:
        """
        Reset controller state for a new analysis.
        """

        self._state.reset()

        self._progress_manager.reset()

    ####################################################################
    # Internal Helper
    ####################################################################

    def _create_thread(
        self,
    ) -> Thread:
        """
        Create the background worker thread.

        The thread is created here so that lifecycle management remains
        centralized inside the controller.
        """

        return Thread(
            target=self._worker.run,
            kwargs={
                "state": self._state,
                "progress_reporter": self._progress_manager,
            },
            daemon=True,
            name="AnalysisWorker",
        )
    ####################################################################
    # Start Analysis
    ####################################################################

    def start(self) -> bool:
        """
        Start a new background analysis.

        Returns
        -------
        bool
            True if analysis started.
            False if already running.
        """

        #
        # Prevent duplicate execution.
        #
        if self._state.is_running:
            return False

        #
        # Clear previous results.
        #
        self._state.analysis_result = None

        self._state.error = None

        self._state.error_message = ""

        self._state.finished_at = None

        self._state.cancelled = False

        #
        # Reset progress.
        #
        self._progress_manager.reset()

        #
        # Mark as preparing.
        #
        self._state.status = AnalysisStatus.PREPARING

        #
        # Create worker thread.
        #
        thread = self._create_thread()

        #
        # Store thread.
        #
        self._state.worker = thread

        #
        # Start execution.
        #
        thread.start()

        return True

    ####################################################################
    # Thread Monitoring
    ####################################################################

    def is_worker_alive(self) -> bool:
        """
        Returns True if worker thread is running.
        """

        worker = self._state.worker

        if worker is None:
            return False

        return worker.is_alive()

    def has_finished(self) -> bool:
        """
        Returns True if worker exists and has completed.
        """

        worker = self._state.worker

        if worker is None:
            return False

        return not worker.is_alive()

    def join(
        self,
        timeout: float | None = None,
    ) -> None:
        """
        Wait for worker completion.
        """

        worker = self._state.worker

        if worker is None:
            return

        worker.join(timeout=timeout)

    ####################################################################
    # State Synchronization
    ####################################################################

    def sync(self) -> None:
        """
        Synchronize runtime state.

        Called repeatedly from Streamlit.

        Responsibilities:
            - Detect worker completion
            - Finalize state
            - Handle errors
        """

        worker = self._state.worker

        if worker is None:
            return

        #
        # Still running.
        #
        if worker.is_alive():
            return

        #
        # Already finalized.
        #
        if self._state.status.is_finished:
            return

        #
        # Worker finished.
        #
        self._finalize()

    ####################################################################
    # Finalization
    ####################################################################

    def _finalize(self) -> None:
        """
        Finalize a completed analysis.

        This method is invoked exactly once after the worker thread exits.
        """

        #
        # Defensive check.
        #
        worker = self._state.worker

        if worker is None:
            return

        #
        # Ensure worker has finished.
        #
        worker.join(timeout=0)

        #
        # Successful execution.
        #
        if self._state.has_result:

            self._state.status = AnalysisStatus.COMPLETED

            self._state.progress = 100

            self._state.message = "Analysis completed successfully."

            return

        #
        # Failed execution.
        #
        if self._state.has_error:

            self._state.status = AnalysisStatus.FAILED

            if not self._state.error_message:
                self._state.error_message = "Analysis failed."

            return

        #
        # Cancelled execution.
        #
        if self._state.cancelled:

            self._state.status = AnalysisStatus.CANCELLED

            self._state.message = "Analysis cancelled."

            return

        #
        # Unexpected termination.
        #
        self._state.status = AnalysisStatus.FAILED

        self._state.error_message = (
            "Analysis terminated unexpectedly."
        )

    ####################################################################
    # Result Access
    ####################################################################

    @property
    def result(self):
        """
        Returns the completed analysis result.
        """

        return self._state.analysis_result

    @property
    def error_message(self) -> str:
        """
        Returns the current error message.
        """

        return self._state.error_message

    ####################################################################
    # Progress Access
    ####################################################################

    @property
    def progress_value(self) -> int:
        """
        Returns the current progress percentage.
        """

        return self._state.progress

    @property
    def progress_message(self) -> str:
        """
        Returns the current progress message.
        """

        return self._state.message

    ####################################################################
    # Duration
    ####################################################################

    @property
    def elapsed_seconds(self) -> float:
        """
        Total elapsed execution time.
        """

        return self._state.duration_seconds

    ####################################################################
    # Cancellation
    ####################################################################

    def cancel(self) -> bool:
        """
        Cancel the currently running analysis.

        Returns
        -------
        bool
            True if a cancellation request was accepted.
            False otherwise.
        """

        if not self._state.status.can_cancel:
            return False

        self._state.cancelled = True

        self._state.status = AnalysisStatus.CANCELLED

        self._state.message = "Cancelling analysis..."

        return True

    ####################################################################
    # Capability Properties
    ####################################################################

    @property
    def can_start(self) -> bool:
        """
        Returns True if a new analysis can be started.
        """

        return (
            self._state.status.can_start
            and self._state.uploaded_file is not None
            and not self.is_worker_alive()
        )

    @property
    def can_cancel(self) -> bool:
        """
        Returns True if the current analysis can be cancelled.
        """

        return (
            self._state.status.can_cancel
            and self.is_worker_alive()
        )

    @property
    def can_reset(self) -> bool:
        """
        Returns True if controller can be reset.
        """

        return (
            not self.is_worker_alive()
            and self._state.status.is_finished
        )

    ####################################################################
    # State Queries
    ####################################################################

    def is_completed(self) -> bool:
        """
        Returns True when analysis completed successfully.
        """

        return self._state.status == AnalysisStatus.COMPLETED

    def is_failed(self) -> bool:
        """
        Returns True when analysis failed.
        """

        return self._state.status == AnalysisStatus.FAILED

    def is_cancelled(self) -> bool:
        """
        Returns True when analysis was cancelled.
        """

        return self._state.status == AnalysisStatus.CANCELLED

    ####################################################################
    # Worker Cleanup
    ####################################################################

    def clear_worker(self) -> None:
        """
        Release worker resources after execution.

        Safe to call multiple times.
        """

        self._state.worker = None

    ####################################################################
    # Diagnostics
    ####################################################################

    def snapshot(self) -> dict[str, object]:
        """
        Returns a diagnostic snapshot of the controller.

        Useful for debugging and logging.
        """

        return {
            "status": self._state.status.value,
            "progress": self._state.progress,
            "message": self._state.message,
            "running": self.is_worker_alive(),
            "completed": self.is_completed(),
            "failed": self.is_failed(),
            "cancelled": self.is_cancelled(),
            "has_result": self._state.has_result,
            "has_error": self._state.has_error,
            "duration": self.elapsed_seconds,
        }

    ####################################################################
    # Cancellation Integration
    ####################################################################

    def request_cancel(self) -> bool:
        """
        Request cancellation of the running analysis.

        The ProgressManager owns the CancellationToken.
        If supported, propagate the request to the pipeline.
        """

        if not self.can_cancel:
            return False

        #
        # Notify the progress manager.
        #
        cancel_method = getattr(
            self._progress_manager,
            "cancel",
            None,
        )

        if callable(cancel_method):
            cancel_method()

        self._state.cancelled = True

        self._state.status = AnalysisStatus.CANCELLED

        self._state.message = "Analysis cancelled."

        return True

    ####################################################################
    # Initialization
    ####################################################################

    def initialize(self) -> None:
        """
        Initialize controller state.

        Safe to call multiple times.
        """

        if self._state.status is None:
            self._state.reset()

    ####################################################################
    # New Analysis
    ####################################################################

    def new_analysis(self) -> None:
        """
        Prepare the controller for a completely new analysis.
        """

        self.clear_worker()

        self.reset()

    ####################################################################
    # Future Extensions
    ####################################################################

    def set_sections(
        self,
        sections: dict[str, Any],
    ) -> None:
        """
        Store extracted paper sections.

        These will be reused by future section agents
        without extracting the paper again.
        """

        self._state.sections = sections

    @property
    def sections(self) -> dict[str, Any]:
        """
        Returns extracted paper sections.
        """

        return self._state.sections

    ####################################################################
    # Debug
    ####################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"status={self._state.status.value!r}, "
            f"progress={self._state.progress}, "
            f"running={self.is_worker_alive()})"
        )