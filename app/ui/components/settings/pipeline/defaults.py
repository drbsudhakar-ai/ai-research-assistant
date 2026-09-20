"""
AI Research Assistant
Pipeline Settings - Default Values

Defines default configuration values for Pipeline Settings.

These defaults are designed around the current
AI Research Assistant architecture:

    app/core/pipeline/
    app/pipeline/
    app/core/progress/

No Streamlit dependency.
No UI logic.
No runtime execution.

Version:
    1.0.0
"""

from __future__ import annotations

from .enums import (
    PipelineExecutionMode,
    AnalysisMode,
    ProgressDisplayMode,
    RetryPolicy,
    PipelineStageType,
    LLMProcessingMode,
    CancellationMode,
    TimeoutPreset,
    ConcurrencyLevel,
)


# ============================================================
# Pipeline Execution Defaults
# ============================================================

DEFAULT_PIPELINE_EXECUTION_MODE = (
    PipelineExecutionMode.SEQUENTIAL
)


DEFAULT_ANALYSIS_MODE = (
    AnalysisMode.RESEARCH
)


# ============================================================
# Pipeline Stage Defaults
# ============================================================

DEFAULT_ENABLED_STAGES: dict[
    PipelineStageType,
    bool,
] = {

    PipelineStageType.PDF_VALIDATION:
        True,

    PipelineStageType.TEXT_PREPARATION:
        True,

    PipelineStageType.PAPER_ANALYSIS:
        True,

    PipelineStageType.HISTORY_STORAGE:
        True,
}


# ============================================================
# Progress Defaults
# ============================================================

DEFAULT_PROGRESS_DISPLAY_MODE = (
    ProgressDisplayMode.DETAILED
)


DEFAULT_CANCELLATION_MODE = (
    CancellationMode.ENABLED
)


# ============================================================
# Error Handling Defaults
# ============================================================

DEFAULT_RETRY_POLICY = (
    RetryPolicy.BASIC
)


DEFAULT_RETRY_COUNT: int = 2


# ============================================================
# Timeout Defaults
# ============================================================

DEFAULT_TIMEOUT_PRESET = (
    TimeoutPreset.NORMAL
)


DEFAULT_TIMEOUT_SECONDS: int = 300


# ============================================================
# LLM Processing Defaults
# ============================================================

DEFAULT_LLM_PROCESSING_MODE = (
    LLMProcessingMode.AUTO
)


# ============================================================
# Performance Defaults
# ============================================================

DEFAULT_CONCURRENCY_LEVEL = (
    ConcurrencyLevel.SINGLE
)


DEFAULT_ENABLE_PARALLEL_PROCESSING: bool = False


DEFAULT_MAX_WORKERS: int = 1


# ============================================================
# Extraction Defaults
# ============================================================

DEFAULT_ENABLE_TITLE_EXTRACTION: bool = True


DEFAULT_ENABLE_TEXT_PREPROCESSING: bool = True


DEFAULT_ENABLE_METADATA_EXTRACTION: bool = True


# ============================================================
# Research Quality Defaults
# ============================================================

DEFAULT_INCLUDE_RESEARCH_GAP: bool = True


DEFAULT_INCLUDE_METHODOLOGY_ANALYSIS: bool = True


DEFAULT_INCLUDE_LIMITATIONS: bool = True


DEFAULT_INCLUDE_FUTURE_WORK: bool = True


DEFAULT_INCLUDE_CITATION_ANALYSIS: bool = True


# ============================================================
# Debug / Development Defaults
# ============================================================

DEFAULT_ENABLE_PIPELINE_LOGGING: bool = True


DEFAULT_VERBOSE_ERRORS: bool = False


# ============================================================
# Export
# ============================================================

__all__ = [

    "DEFAULT_PIPELINE_EXECUTION_MODE",

    "DEFAULT_ANALYSIS_MODE",

    "DEFAULT_ENABLED_STAGES",

    "DEFAULT_PROGRESS_DISPLAY_MODE",

    "DEFAULT_CANCELLATION_MODE",

    "DEFAULT_RETRY_POLICY",

    "DEFAULT_RETRY_COUNT",

    "DEFAULT_TIMEOUT_PRESET",

    "DEFAULT_TIMEOUT_SECONDS",

    "DEFAULT_LLM_PROCESSING_MODE",

    "DEFAULT_CONCURRENCY_LEVEL",

    "DEFAULT_ENABLE_PARALLEL_PROCESSING",

    "DEFAULT_MAX_WORKERS",

    "DEFAULT_ENABLE_TITLE_EXTRACTION",

    "DEFAULT_ENABLE_TEXT_PREPROCESSING",

    "DEFAULT_ENABLE_METADATA_EXTRACTION",

    "DEFAULT_INCLUDE_RESEARCH_GAP",

    "DEFAULT_INCLUDE_METHODOLOGY_ANALYSIS",

    "DEFAULT_INCLUDE_LIMITATIONS",

    "DEFAULT_INCLUDE_FUTURE_WORK",

    "DEFAULT_INCLUDE_CITATION_ANALYSIS",

    "DEFAULT_ENABLE_PIPELINE_LOGGING",

    "DEFAULT_VERBOSE_ERRORS",
]