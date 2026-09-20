"""
AI Research Assistant

File: app/ui/components/settings/pipeline/enums.py
Pipeline Settings - Enumerations

Defines controlled values used by Pipeline Settings.

This module contains:
    - Pipeline execution options
    - Processing modes
    - Progress display options
    - Retry policies
    - Resource management options

No UI logic.
No Streamlit dependency.
No state management.

Version:
    1.0.0
"""

from __future__ import annotations

from enum import Enum


# ============================================================
# Pipeline Execution
# ============================================================


class PipelineExecutionMode(str, Enum):
    """
    Defines how pipeline stages execute.
    """

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


# ============================================================
# Analysis Mode
# ============================================================


class AnalysisMode(str, Enum):
    """
    Defines analysis depth.

    Fast mode is useful for quick previews.
    Research mode targets detailed paper analysis.
    """

    FAST = "fast"
    RESEARCH = "research"


# ============================================================
# Progress Display
# ============================================================


class ProgressDisplayMode(str, Enum):
    """
    Controls progress visualization.
    """

    DETAILED = "detailed"
    COMPACT = "compact"
    HIDDEN = "hidden"


# ============================================================
# Retry Behaviour
# ============================================================


class RetryPolicy(str, Enum):
    """
    Defines pipeline retry strategy.
    """

    NONE = "none"
    BASIC = "basic"
    AGGRESSIVE = "aggressive"


# ============================================================
# Pipeline Stage Control
# ============================================================


class PipelineStageType(str, Enum):
    """
    Available research pipeline stages.

    Maps to existing pipeline steps:

        ValidatePdfStep
        PreparePaperStep
        AnalyzePaperStep
        SaveHistoryStep
    """

    PDF_VALIDATION = "pdf_validation"

    TEXT_PREPARATION = "text_preparation"

    PAPER_ANALYSIS = "paper_analysis"

    HISTORY_STORAGE = "history_storage"


# ============================================================
# LLM Processing Strategy
# ============================================================


class LLMProcessingMode(str, Enum):
    """
    Controls LLM execution strategy.
    """

    LOCAL = "local"
    CLOUD = "cloud"
    AUTO = "auto"


# ============================================================
# Cancellation Behaviour
# ============================================================


class CancellationMode(str, Enum):
    """
    Defines pipeline cancellation behaviour.
    """

    ENABLED = "enabled"
    DISABLED = "disabled"


# ============================================================
# Timeout Presets
# ============================================================


class TimeoutPreset(str, Enum):
    """
    Common pipeline timeout values.

    Values are stored as seconds.
    """

    SHORT = "60"

    NORMAL = "300"

    LONG = "600"

    EXTENDED = "1200"


# ============================================================
# Concurrency Level
# ============================================================


class ConcurrencyLevel(str, Enum):
    """
    Maximum parallel worker count.
    """

    SINGLE = "1"

    LOW = "2"

    MEDIUM = "4"

    HIGH = "8"


# ============================================================
# Exported Symbols
# ============================================================


__all__ = [
    "PipelineExecutionMode",
    "AnalysisMode",
    "ProgressDisplayMode",
    "RetryPolicy",
    "PipelineStageType",
    "LLMProcessingMode",
    "CancellationMode",
    "TimeoutPreset",
    "ConcurrencyLevel",
]