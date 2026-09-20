"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Manager
File         : progress_manager.py
Version      : 3.0.0

Description:
    Thread-safe progress state manager.

    Acts as the runtime bridge between pipeline execution
    and UI rendering.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threading import Lock
from time import perf_counter



from app.core.progress.progress_reporter import (
    ProgressReporter,
)

from app.core.progress.progress_stage import ProgressStage
from app.core.progress.progress_state import (
    ProgressState,
)

from app.core.progress.cancellation_token import (
    CancellationToken,
)


__all__ = [
    "ProgressManager",
]



class ProgressManager(ProgressReporter):
    """
    Thread-safe progress manager.

    Receives progress events from pipeline execution
    and exposes current state to UI components.
    """

    VERSION = "3.0.0"


    def __init__(
        self,
        cancellation_token: CancellationToken | None = None,
    ) -> None:
        """
        Initialize progress manager.

        Parameters
        ----------
        cancellation_token:
            Optional cancellation controller.
        """

        self._lock = Lock()

        self._state = ProgressState()

        self._start_time = perf_counter()

        self._cancellation_token = (
            cancellation_token
            or CancellationToken()
        )



    # ------------------------------------------------------------------
    # ProgressReporter implementation
    # ------------------------------------------------------------------

    def update(
        self,
        message: str,
        percentage: float | None = None,
        stage: ProgressStage  | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Update progress state.

        Thread safe.
        """
        with self._lock:

            if percentage is not None:

                self._state.percentage = max(
                    0,
                    min(
                        100,
                        percentage,
                    ),
                )


            if stage is not None:

                self._state.stage = stage

            if metadata is not None:
                self._state.metadata = metadata.copy()


            self._state.status = message

            self._state.elapsed_seconds = (
                perf_counter() - self._start_time
            )


    # ------------------------------------------------------------------
    # State access
    # ------------------------------------------------------------------

    def get_state(
        self,
    ) -> ProgressState:
        """
        Return current progress snapshot.
        """

        with self._lock:

            return ProgressState(
                stage=self._state.stage,

                percentage=self._state.percentage,

                status=self._state.status,

                elapsed_seconds=self._state.elapsed_seconds,

                completed=self._state.completed,

                cancelled=self._state.cancelled,

                failed=self._state.failed,

                error_message=self._state.error_message,
            )



    # ------------------------------------------------------------------
    # Cancellation
    # ------------------------------------------------------------------

    def cancel(
        self,
    ) -> None:
        """
        Request cancellation.
        """

        self._cancellation_token.cancel()



    def is_cancelled(
        self,
    ) -> bool:
        """
        Check cancellation status.
        """

        return (
            self._cancellation_token
            .is_cancelled()
        )



    @property
    def cancellation_token(
        self,
    ) -> CancellationToken:
        """
        Access cancellation token.
        """

        return self._cancellation_token



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset progress state.
        """

        with self._lock:

            self._state = ProgressState()

            self._start_time = perf_counter()



    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Manager name.
        """

        return "Progress Manager"



    @property
    def version(
        self,
    ) -> str:
        """
        Version.
        """

        return self.VERSION