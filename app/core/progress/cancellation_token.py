"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Framework
File         : cancellation_token.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Provides cooperative cancellation support for long-running workflows.

Responsibilities:
    - Signal cancellation requests.
    - Allow workflow components to check cancellation state.

Notes:
    - Thread-safe implementation.
    - UI independent.
===============================================================================
"""

from __future__ import annotations

from threading import Event


class CancellationToken:
    """
    Cooperative cancellation token.
    """

    def __init__(self) -> None:

        self._event = Event()

    @property
    def cancelled(self) -> bool:
        """
        Returns True if cancellation was requested.
        """

        return self._event.is_set()

    def is_cancelled(self) -> bool:
        """
        Backward-compatible API for pipeline components.
        """
        return self.cancelled

    def cancel(self) -> None:
        """
        Request workflow cancellation.

        This sets CANCEL_REQUESTED at the token level. It does not mean
        the worker has stopped. Do not report CANCELLED until the worker
        is no longer running (T011/T012).
        """

        self._event.set()

    def reset(self) -> None:
        """
        Clear cancellation request.
        """

        self._event.clear()

    def throw_if_cancelled(self) -> None:
        """
        Raise an exception if cancelled.
        """

        if self.cancelled:
            raise RuntimeError("Analysis was cancelled by the user.")
