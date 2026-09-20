"""
AI Research Assistant
Pipeline Settings - Validators

Provides validation rules for Pipeline Settings.

Validates:
    - Pipeline execution options
    - Enabled stages
    - Retry configuration
    - Timeout values
    - Performance settings
    - Resource limits

No Streamlit dependency.
No UI logic.
No runtime execution.

Version:
    1.0.0
"""

from __future__ import annotations

from typing import Any

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
# Generic Helpers
# ============================================================


def validate_enum_value(
    value: object,
    enum_type: type,
) -> tuple[bool, str]:
    """
    Validate enum based configuration values.
    """

    if isinstance(
        value,
        enum_type,
    ):
        return True, ""

    return (
        False,
        (
            f"Invalid value '{value}'. "
            f"Expected {enum_type.__name__}."
        ),
    )


# ============================================================
# Pipeline Mode Validation
# ============================================================


def validate_execution_mode(
    value: PipelineExecutionMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        PipelineExecutionMode,
    )


def validate_analysis_mode(
    value: AnalysisMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        AnalysisMode,
    )


def validate_progress_mode(
    value: ProgressDisplayMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        ProgressDisplayMode,
    )


def validate_llm_processing_mode(
    value: LLMProcessingMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        LLMProcessingMode,
    )


# ============================================================
# Pipeline Stage Validation
# ============================================================


def validate_enabled_stages(
    stages: dict[PipelineStageType, bool],
) -> tuple[bool, str]:
    """
    Validate pipeline stage configuration.
    """

    if not isinstance(
        stages,
        dict,
    ):
        return (
            False,
            "Pipeline stages must be a dictionary.",
        )


    for stage, enabled in stages.items():

        if not isinstance(
            stage,
            PipelineStageType,
        ):
            return (
                False,
                f"Invalid pipeline stage: {stage}",
            )


        if not isinstance(
            enabled,
            bool,
        ):
            return (
                False,
                (
                    f"Stage '{stage}' "
                    "must contain boolean value."
                ),
            )


    # Analysis cannot run without preparation
    if (
        stages.get(
            PipelineStageType.PAPER_ANALYSIS,
            False,
        )
        and not stages.get(
            PipelineStageType.TEXT_PREPARATION,
            False,
        )
    ):
        return (
            False,
            (
                "Paper analysis requires "
                "text preparation stage."
            ),
        )


    return True, ""


# ============================================================
# Retry Validation
# ============================================================


def validate_retry_policy(
    value: RetryPolicy,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        RetryPolicy,
    )


def validate_retry_count(
    retry_count: int,
) -> tuple[bool, str]:
    """
    Validate retry count.
    """

    if not isinstance(
        retry_count,
        int,
    ):
        return (
            False,
            "Retry count must be an integer.",
        )


    if retry_count < 0:
        return (
            False,
            "Retry count cannot be negative.",
        )


    if retry_count > 10:
        return (
            False,
            "Retry count cannot exceed 10.",
        )


    return True, ""


# ============================================================
# Timeout Validation
# ============================================================


def validate_timeout_preset(
    value: TimeoutPreset,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        TimeoutPreset,
    )


def validate_timeout_seconds(
    seconds: int,
) -> tuple[bool, str]:
    """
    Validate execution timeout.
    """

    if not isinstance(
        seconds,
        int,
    ):
        return (
            False,
            "Timeout must be an integer.",
        )


    if seconds < 30:
        return (
            False,
            "Timeout should be at least 30 seconds.",
        )


    if seconds > 3600:
        return (
            False,
            "Timeout cannot exceed 1 hour.",
        )


    return True, ""


# ============================================================
# Performance Validation
# ============================================================


def validate_concurrency_level(
    value: ConcurrencyLevel,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        ConcurrencyLevel,
    )


def validate_worker_count(
    workers: int,
) -> tuple[bool, str]:
    """
    Validate worker count.
    """

    if not isinstance(
        workers,
        int,
    ):
        return (
            False,
            "Worker count must be integer.",
        )


    if workers < 1:
        return (
            False,
            "Worker count must be at least 1.",
        )


    if workers > 16:
        return (
            False,
            "Worker count cannot exceed 16.",
        )


    return True, ""


def validate_parallel_execution(
    execution_mode: PipelineExecutionMode,
    enable_parallel: bool,
) -> tuple[bool, str]:
    """
    Validate parallel execution settings.
    """

    if (
        enable_parallel
        and execution_mode
        != PipelineExecutionMode.PARALLEL
    ):
        return (
            False,
            (
                "Parallel processing requires "
                "parallel execution mode."
            ),
        )


    return True, ""


# ============================================================
# Cancellation Validation
# ============================================================


def validate_cancellation_mode(
    value: CancellationMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        CancellationMode,
    )


# ============================================================
# Complete Validation
# ============================================================


def validate_pipeline_settings(
    settings: dict[str, Any],
) -> tuple[bool, list[str]]:
    """
    Validate complete Pipeline Settings.

    Returns:
        (
            is_valid,
            errors
        )
    """

    errors: list[str] = []


    enum_validators = [

        (
            "execution_mode",
            validate_execution_mode,
        ),

        (
            "analysis_mode",
            validate_analysis_mode,
        ),

        (
            "progress_display_mode",
            validate_progress_mode,
        ),

        (
            "llm_processing_mode",
            validate_llm_processing_mode,
        ),

        (
            "retry_policy",
            validate_retry_policy,
        ),

        (
            "timeout_preset",
            validate_timeout_preset,
        ),

        (
            "concurrency_level",
            validate_concurrency_level,
        ),

        (
            "cancellation_mode",
            validate_cancellation_mode,
        ),
    ]


    for key, validator in enum_validators:

        if key in settings:

            valid, message = validator(
                settings[key]
            )

            if not valid:

                errors.append(
                    f"{key}: {message}"
                )


    if "enabled_stages" in settings:

        valid, message = (
            validate_enabled_stages(
                settings["enabled_stages"]
            )
        )

        if not valid:

            errors.append(
                f"enabled_stages: {message}"
            )


    if "retry_count" in settings:

        valid, message = (
            validate_retry_count(
                settings["retry_count"]
            )
        )

        if not valid:

            errors.append(
                f"retry_count: {message}"
            )


    if "timeout_seconds" in settings:

        valid, message = (
            validate_timeout_seconds(
                settings["timeout_seconds"]
            )
        )

        if not valid:

            errors.append(
                f"timeout_seconds: {message}"
            )


    if "max_workers" in settings:

        valid, message = (
            validate_worker_count(
                settings["max_workers"]
            )
        )

        if not valid:

            errors.append(
                f"max_workers: {message}"
            )


    if (
        "execution_mode" in settings
        and "enable_parallel_processing" in settings
    ):

        valid, message = (
            validate_parallel_execution(
                settings["execution_mode"],
                settings["enable_parallel_processing"],
            )
        )

        if not valid:

            errors.append(
                f"parallel_processing: {message}"
            )


    return (
        len(errors) == 0,
        errors,
    )


# ============================================================
# Export
# ============================================================


__all__ = [

    "validate_enum_value",

    "validate_execution_mode",

    "validate_analysis_mode",

    "validate_progress_mode",

    "validate_llm_processing_mode",

    "validate_enabled_stages",

    "validate_retry_policy",

    "validate_retry_count",

    "validate_timeout_preset",

    "validate_timeout_seconds",

    "validate_concurrency_level",

    "validate_worker_count",

    "validate_parallel_execution",

    "validate_cancellation_mode",

    "validate_pipeline_settings",
]