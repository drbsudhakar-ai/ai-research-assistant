"""
AI Research Assistant
Pipeline Settings - Metadata Definitions

Provides UI metadata for Pipeline Settings options.

Contains:
    - Display labels
    - Descriptions
    - Help text
    - Icons

No Streamlit dependency.
No state handling.
No business logic.

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass

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
# Metadata Model
# ============================================================


@dataclass(frozen=True)
class SettingMetadata:
    """
    Common metadata model for pipeline settings.
    """

    label: str
    description: str
    help_text: str
    icon: str | None = None


# ============================================================
# Pipeline Execution Metadata
# ============================================================


PIPELINE_EXECUTION_METADATA: dict[
    PipelineExecutionMode,
    SettingMetadata,
] = {

    PipelineExecutionMode.SEQUENTIAL:
        SettingMetadata(
            label="Sequential Execution",
            description=(
                "Runs pipeline stages one after another."
            ),
            help_text=(
                "Recommended for stable research workflows."
            ),
            icon="➡️",
        ),

    PipelineExecutionMode.PARALLEL:
        SettingMetadata(
            label="Parallel Execution",
            description=(
                "Runs independent tasks simultaneously."
            ),
            help_text=(
                "Improves speed for supported workloads."
            ),
            icon="⚡",
        ),
}


# ============================================================
# Analysis Mode Metadata
# ============================================================


ANALYSIS_MODE_METADATA: dict[
    AnalysisMode,
    SettingMetadata,
] = {

    AnalysisMode.FAST:
        SettingMetadata(
            label="Fast Analysis",
            description=(
                "Provides quick paper analysis "
                "with reduced processing depth."
            ),
            help_text=(
                "Useful for previews and testing."
            ),
            icon="🚀",
        ),

    AnalysisMode.RESEARCH:
        SettingMetadata(
            label="Research Quality Analysis",
            description=(
                "Performs deeper academic analysis "
                "for research workflows."
            ),
            help_text=(
                "Recommended for final reports."
            ),
            icon="🔬",
        ),
}


# ============================================================
# Progress Display Metadata
# ============================================================


PROGRESS_DISPLAY_METADATA: dict[
    ProgressDisplayMode,
    SettingMetadata,
] = {

    ProgressDisplayMode.DETAILED:
        SettingMetadata(
            label="Detailed Progress",
            description=(
                "Shows stage-by-stage execution progress."
            ),
            help_text=(
                "Displays pipeline steps and status."
            ),
            icon="📊",
        ),

    ProgressDisplayMode.COMPACT:
        SettingMetadata(
            label="Compact Progress",
            description=(
                "Shows simplified progress information."
            ),
            help_text=(
                "Cleaner interface with fewer details."
            ),
            icon="📈",
        ),

    ProgressDisplayMode.HIDDEN:
        SettingMetadata(
            label="Hidden Progress",
            description=(
                "Runs pipeline without progress display."
            ),
            help_text=(
                "Useful for automated execution."
            ),
            icon="⚪",
        ),
}


# ============================================================
# Retry Policy Metadata
# ============================================================


RETRY_POLICY_METADATA: dict[
    RetryPolicy,
    SettingMetadata,
] = {

    RetryPolicy.NONE:
        SettingMetadata(
            label="No Retry",
            description=(
                "Stops execution after first failure."
            ),
            help_text=(
                "Useful for debugging."
            ),
            icon="⛔",
        ),

    RetryPolicy.BASIC:
        SettingMetadata(
            label="Basic Retry",
            description=(
                "Retries failed operations once."
            ),
            help_text=(
                "Recommended default."
            ),
            icon="🔄",
        ),

    RetryPolicy.AGGRESSIVE:
        SettingMetadata(
            label="Aggressive Retry",
            description=(
                "Retries failed operations multiple times."
            ),
            help_text=(
                "Useful for unstable providers."
            ),
            icon="♻️",
        ),
}


# ============================================================
# Pipeline Stage Metadata
# ============================================================


PIPELINE_STAGE_METADATA: dict[
    PipelineStageType,
    SettingMetadata,
] = {

    PipelineStageType.PDF_VALIDATION:
        SettingMetadata(
            label="PDF Validation",
            description=(
                "Validates uploaded research papers."
            ),
            help_text=(
                "Checks file format and availability."
            ),
            icon="📄",
        ),

    PipelineStageType.TEXT_PREPARATION:
        SettingMetadata(
            label="Text Preparation",
            description=(
                "Extracts and prepares paper content."
            ),
            help_text=(
                "Runs PDF extraction and preprocessing."
            ),
            icon="📝",
        ),

    PipelineStageType.PAPER_ANALYSIS:
        SettingMetadata(
            label="AI Paper Analysis",
            description=(
                "Generates research analysis using LLM."
            ),
            help_text=(
                "Main intelligence processing stage."
            ),
            icon="🤖",
        ),

    PipelineStageType.HISTORY_STORAGE:
        SettingMetadata(
            label="History Storage",
            description=(
                "Stores completed analysis results."
            ),
            help_text=(
                "Saves records for future review."
            ),
            icon="💾",
        ),
}


# ============================================================
# LLM Processing Metadata
# ============================================================


LLM_PROCESSING_METADATA: dict[
    LLMProcessingMode,
    SettingMetadata,
] = {

    LLMProcessingMode.LOCAL:
        SettingMetadata(
            label="Local Model",
            description=(
                "Uses locally hosted AI models."
            ),
            help_text=(
                "Best for privacy and offline usage."
            ),
            icon="💻",
        ),

    LLMProcessingMode.CLOUD:
        SettingMetadata(
            label="Cloud Provider",
            description=(
                "Uses external AI providers."
            ),
            help_text=(
                "Provides access to larger models."
            ),
            icon="☁️",
        ),

    LLMProcessingMode.AUTO:
        SettingMetadata(
            label="Automatic Selection",
            description=(
                "Automatically selects available provider."
            ),
            help_text=(
                "Balances performance and availability."
            ),
            icon="🔀",
        ),
}


# ============================================================
# Cancellation Metadata
# ============================================================


CANCELLATION_METADATA: dict[
    CancellationMode,
    SettingMetadata,
] = {

    CancellationMode.ENABLED:
        SettingMetadata(
            label="Enable Cancellation",
            description=(
                "Allows users to stop running pipelines."
            ),
            help_text=(
                "Recommended for long analyses."
            ),
            icon="🛑",
        ),

    CancellationMode.DISABLED:
        SettingMetadata(
            label="Disable Cancellation",
            description=(
                "Pipeline runs without interruption."
            ),
            help_text=(
                "Useful for automated jobs."
            ),
            icon="▶️",
        ),
}


# ============================================================
# Timeout Metadata
# ============================================================


TIMEOUT_METADATA: dict[
    TimeoutPreset,
    SettingMetadata,
] = {

    TimeoutPreset.SHORT:
        SettingMetadata(
            label="Short (1 minute)",
            description=(
                "Fast timeout for lightweight tasks."
            ),
            help_text=(
                "Suitable for quick tests."
            ),
            icon="⏱️",
        ),

    TimeoutPreset.NORMAL:
        SettingMetadata(
            label="Normal (5 minutes)",
            description=(
                "Balanced execution timeout."
            ),
            help_text=(
                "Recommended default."
            ),
            icon="⏳",
        ),

    TimeoutPreset.LONG:
        SettingMetadata(
            label="Long (10 minutes)",
            description=(
                "Allows extended processing."
            ),
            help_text=(
                "Suitable for large papers."
            ),
            icon="⌛",
        ),

    TimeoutPreset.EXTENDED:
        SettingMetadata(
            label="Extended (20 minutes)",
            description=(
                "Maximum processing duration."
            ),
            help_text=(
                "For very large research documents."
            ),
            icon="🕒",
        ),
}


# ============================================================
# Concurrency Metadata
# ============================================================


CONCURRENCY_METADATA: dict[
    ConcurrencyLevel,
    SettingMetadata,
] = {

    ConcurrencyLevel.SINGLE:
        SettingMetadata(
            label="Single Worker",
            description=(
                "Runs one task at a time."
            ),
            help_text=(
                "Best for low-resource systems."
            ),
            icon="1️⃣",
        ),

    ConcurrencyLevel.LOW:
        SettingMetadata(
            label="2 Workers",
            description=(
                "Uses limited parallel execution."
            ),
            help_text=(
                "Balanced resource usage."
            ),
            icon="2️⃣",
        ),

    ConcurrencyLevel.MEDIUM:
        SettingMetadata(
            label="4 Workers",
            description=(
                "Uses moderate parallel execution."
            ),
            help_text=(
                "Recommended for capable systems."
            ),
            icon="4️⃣",
        ),

    ConcurrencyLevel.HIGH:
        SettingMetadata(
            label="8 Workers",
            description=(
                "Maximum parallel execution."
            ),
            help_text=(
                "Requires higher system resources."
            ),
            icon="8️⃣",
        ),
}


# ============================================================
# Export
# ============================================================

__all__ = [
    "SettingMetadata",
    "PIPELINE_EXECUTION_METADATA",
    "ANALYSIS_MODE_METADATA",
    "PROGRESS_DISPLAY_METADATA",
    "RETRY_POLICY_METADATA",
    "PIPELINE_STAGE_METADATA",
    "LLM_PROCESSING_METADATA",
    "CANCELLATION_METADATA",
    "TIMEOUT_METADATA",
    "CONCURRENCY_METADATA",
]