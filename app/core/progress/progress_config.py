"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Framework
File         : progress_config.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Central configuration for workflow progress.

Responsibilities:
    - Define progress percentages.
    - Define default status messages.
    - Provide helper functions for retrieving configuration.

Notes:
    - Contains no business logic.
    - Immutable configuration only.
    - Shared across all workflows.
===============================================================================
"""

from __future__ import annotations

from typing import Final

from app.core.progress.progress_stage import ProgressStage

__all__ = [
    "PROGRESS_PERCENTAGES",
    "PROGRESS_MESSAGES",
    "DEFAULT_PROGRESS_PERCENTAGE",
    "DEFAULT_PROGRESS_MESSAGE",
    "get_progress_percentage",
    "get_progress_message",
]

# ============================================================================
# Defaults
# ============================================================================

DEFAULT_PROGRESS_PERCENTAGE: Final[int] = 0

DEFAULT_PROGRESS_MESSAGE: Final[str] = "Working..."

DEFAULT_STAGE: Final[ProgressStage] = ProgressStage.STARTING

# ============================================================================
# Progress Percentages
# ============================================================================

PROGRESS_PERCENTAGES: Final[dict[ProgressStage, int]] = {
    ProgressStage.STARTING: 0,
    ProgressStage.VALIDATING: 5,
    ProgressStage.EXTRACTING_TEXT: 20,
    ProgressStage.EXTRACTING_TITLE: 35,
    ProgressStage.PREPROCESSING: 50,
    ProgressStage.BUILDING_CONTEXT: 60,
    ProgressStage.ANALYZING: 80,
    ProgressStage.SAVING: 95,
    ProgressStage.COMPLETED: 100,
    ProgressStage.FAILED: 100,
    ProgressStage.CANCELLED: 100,
}

# ============================================================================
# Default Messages
# ============================================================================

PROGRESS_MESSAGES: Final[dict[ProgressStage, str]] = {
    ProgressStage.STARTING:
        "🚀 Starting analysis...",

    ProgressStage.VALIDATING:
        "📄 Validating uploaded PDF...",

    ProgressStage.EXTRACTING_TEXT:
        "📚 Extracting paper text...",

    ProgressStage.EXTRACTING_TITLE:
        "🏷 Extracting paper title...",

    ProgressStage.PREPROCESSING:
        "📝 Preparing research paper...",

    ProgressStage.BUILDING_CONTEXT:
        "📋 Building AI analysis context...",

    ProgressStage.ANALYZING:
        "🤖 Generating AI analysis...",

    ProgressStage.SAVING:
        "💾 Saving analysis history...",

    ProgressStage.COMPLETED:
        "✅ Analysis completed successfully.",

    ProgressStage.FAILED:
        "❌ Analysis failed.",

    ProgressStage.CANCELLED:
        "⛔ Analysis cancelled.",
}

# ============================================================================
# Helper Functions
# ============================================================================


def get_progress_percentage(stage: ProgressStage) -> int:
    """
    Return the configured percentage for a workflow stage.

    Parameters
    ----------
    stage
        Workflow stage.

    Returns
    -------
    int
        Progress percentage.
    """

    return PROGRESS_PERCENTAGES.get(
        stage,
        DEFAULT_PROGRESS_PERCENTAGE,
    )


def get_progress_message(stage: ProgressStage) -> str:
    """
    Return the default message for a workflow stage.

    Parameters
    ----------
    stage
        Workflow stage.

    Returns
    -------
    str
        Default status message.
    """

    return PROGRESS_MESSAGES.get(
        stage,
        DEFAULT_PROGRESS_MESSAGE,
    )