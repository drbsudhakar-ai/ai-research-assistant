"""Canonical analysis lifecycle status.

This enum is the job/analysis status vocabulary. It is not a progress
stage and not a pipeline execution status.

``CANCEL_REQUESTED`` means cancellation was asked for; the worker may
still be running. ``CANCELLED`` means the worker has actually stopped.

Job registry and cancel completion remain T011/T012. This module only
defines the vocabulary.
"""

from __future__ import annotations

from enum import StrEnum


class AnalysisStatus(StrEnum):
    """Lifecycle state of an analysis execution."""

    IDLE = "idle"
    PREPARING = "preparing"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCEL_REQUESTED = "cancel_requested"
    CANCELLED = "cancelled"

    @property
    def is_active(self) -> bool:
        """True while work may still be in progress, including cancel-requested."""

        return self in {
            AnalysisStatus.PREPARING,
            AnalysisStatus.RUNNING,
            AnalysisStatus.CANCEL_REQUESTED,
        }

    @property
    def is_finished(self) -> bool:
        """True after the worker has stopped (success, failure, or cancelled)."""

        return self in {
            AnalysisStatus.COMPLETED,
            AnalysisStatus.FAILED,
            AnalysisStatus.CANCELLED,
        }

    @property
    def can_start(self) -> bool:
        """True when a new analysis may be started."""

        return self in {
            AnalysisStatus.IDLE,
            AnalysisStatus.COMPLETED,
            AnalysisStatus.FAILED,
            AnalysisStatus.CANCELLED,
        }

    @property
    def can_cancel(self) -> bool:
        """True when a cancellation request may still be issued."""

        return self in {
            AnalysisStatus.PREPARING,
            AnalysisStatus.RUNNING,
        }

    @property
    def display_name(self) -> str:
        return {
            AnalysisStatus.IDLE: "Idle",
            AnalysisStatus.PREPARING: "Preparing",
            AnalysisStatus.RUNNING: "Running",
            AnalysisStatus.COMPLETED: "Completed",
            AnalysisStatus.FAILED: "Failed",
            AnalysisStatus.CANCEL_REQUESTED: "Cancellation requested",
            AnalysisStatus.CANCELLED: "Cancelled",
        }[self]
