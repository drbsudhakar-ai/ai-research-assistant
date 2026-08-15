"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Lifecycle
File         : analysis_status.py
Version      : 4.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines the lifecycle states for an analysis execution.

Purpose:
    Replace multiple Streamlit session-state boolean flags with a single,
    strongly typed state machine.

Benefits:
    - Prevents invalid state combinations.
    - Simplifies UI rendering.
    - Supports rerun-safe execution.
    - Supports future cancellation.
    - Supports future parallel section analysis.
    - Provider independent.

State Flow:

    IDLE
      │
      ▼
    PREPARING
      │
      ▼
    RUNNING
      │
      ├──────────────► CANCELLED
      │
      ├──────────────► FAILED
      │
      ▼
    COMPLETED

===============================================================================
"""

from __future__ import annotations

from enum import StrEnum


class AnalysisStatus(StrEnum):
    """
    Represents the lifecycle state of an analysis request.

    The UI should render entirely based on this state instead of relying on
    multiple boolean flags such as:

        analysis_running
        analysis_completed
        analysis_failed

    This guarantees that only one valid lifecycle state exists at any time.
    """

    # ------------------------------------------------------------------
    # No analysis has started.
    # ------------------------------------------------------------------
    IDLE = "idle"

    # ------------------------------------------------------------------
    # Preparing the analysis.
    #
    # Examples:
    #   - Validate uploaded PDF
    #   - Extract paper
    #   - Initialize pipeline
    # ------------------------------------------------------------------
    PREPARING = "preparing"

    # ------------------------------------------------------------------
    # Analysis pipeline is actively running.
    # ------------------------------------------------------------------
    RUNNING = "running"

    # ------------------------------------------------------------------
    # Analysis completed successfully.
    # ------------------------------------------------------------------
    COMPLETED = "completed"

    # ------------------------------------------------------------------
    # Analysis terminated because of an error.
    # ------------------------------------------------------------------
    FAILED = "failed"

    # ------------------------------------------------------------------
    # Analysis cancelled by the user after the worker has actually stopped.
    #
    # CANCEL_REQUESTED is not a status on this enum yet (T011/T012).
    # Callers must not treat a cancellation *request* as CANCELLED while
    # the worker is still alive. Current controllers still assign
    # CANCELLED immediately on request; that is a known defect, not
    # accepted semantics.
    # ------------------------------------------------------------------
    CANCELLED = "cancelled"

    @property
    def is_active(self) -> bool:
        """
        Returns True while an analysis is actively executing.
        """
        return self in (
            AnalysisStatus.PREPARING,
            AnalysisStatus.RUNNING,
        )

    @property
    def is_finished(self) -> bool:
        """
        Returns True when execution has ended.

        Includes:
            COMPLETED
            FAILED
            CANCELLED
        """
        return self in (
            AnalysisStatus.COMPLETED,
            AnalysisStatus.FAILED,
            AnalysisStatus.CANCELLED,
        )

    @property
    def can_start(self) -> bool:
        """
        Returns True if a new analysis can be started.
        """
        return self in (
            AnalysisStatus.IDLE,
            AnalysisStatus.COMPLETED,
            AnalysisStatus.FAILED,
            AnalysisStatus.CANCELLED,
        )

    @property
    def can_cancel(self) -> bool:
        """
        Returns True if the current analysis can be cancelled.
        """
        return self in (
            AnalysisStatus.PREPARING,
            AnalysisStatus.RUNNING,
        )

    @property
    def display_name(self) -> str:
        """
        Human-readable display name for the UI.
        """
        return {
            AnalysisStatus.IDLE: "Idle",
            AnalysisStatus.PREPARING: "Preparing",
            AnalysisStatus.RUNNING: "Running",
            AnalysisStatus.COMPLETED: "Completed",
            AnalysisStatus.FAILED: "Failed",
            AnalysisStatus.CANCELLED: "Cancelled",
        }[self]
