"""
AI Research Assistant
Pipeline Settings State

Central state container for Pipeline Settings.

Responsibilities:
    - Store pipeline configuration
    - Provide default initialization
    - Track modifications
    - Validate configuration
    - Reset to defaults
    - Export configuration

No Streamlit dependency.
No UI logic.

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
    asdict,
)
from pathlib import Path
from typing import Any

from ..defaults import (
    DEFAULT_PIPELINE_EXECUTION_MODE,
    DEFAULT_ANALYSIS_MODE,
    DEFAULT_ENABLED_STAGES,
    DEFAULT_PROGRESS_DISPLAY_MODE,
    DEFAULT_CANCELLATION_MODE,
    DEFAULT_RETRY_POLICY,
    DEFAULT_RETRY_COUNT,
    DEFAULT_TIMEOUT_PRESET,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_LLM_PROCESSING_MODE,
    DEFAULT_CONCURRENCY_LEVEL,
    DEFAULT_ENABLE_PARALLEL_PROCESSING,
    DEFAULT_MAX_WORKERS,
    DEFAULT_ENABLE_TITLE_EXTRACTION,
    DEFAULT_ENABLE_TEXT_PREPROCESSING,
    DEFAULT_ENABLE_METADATA_EXTRACTION,
    DEFAULT_INCLUDE_RESEARCH_GAP,
    DEFAULT_INCLUDE_METHODOLOGY_ANALYSIS,
    DEFAULT_INCLUDE_LIMITATIONS,
    DEFAULT_INCLUDE_FUTURE_WORK,
    DEFAULT_INCLUDE_CITATION_ANALYSIS,
    DEFAULT_ENABLE_PIPELINE_LOGGING,
    DEFAULT_VERBOSE_ERRORS,
)

from ..enums import (
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

from ..validators import (
    validate_pipeline_settings,
)


@dataclass
class PipelineSettingsState:
    """
    Runtime state for Pipeline Settings.
    """


    # ========================================================
    # Pipeline Execution
    # ========================================================

    execution_mode: PipelineExecutionMode = (
        DEFAULT_PIPELINE_EXECUTION_MODE
    )

    analysis_mode: AnalysisMode = (
        DEFAULT_ANALYSIS_MODE
    )


    enabled_stages: dict[
        PipelineStageType,
        bool,
    ] = field(
        default_factory=lambda:
            DEFAULT_ENABLED_STAGES.copy()
    )


    # ========================================================
    # Progress Management
    # ========================================================

    progress_display_mode: ProgressDisplayMode = (
        DEFAULT_PROGRESS_DISPLAY_MODE
    )

    cancellation_mode: CancellationMode = (
        DEFAULT_CANCELLATION_MODE
    )


    # ========================================================
    # Error Handling
    # ========================================================

    retry_policy: RetryPolicy = (
        DEFAULT_RETRY_POLICY
    )

    retry_count: int = (
        DEFAULT_RETRY_COUNT
    )


    # ========================================================
    # Timeout
    # ========================================================

    timeout_preset: TimeoutPreset = (
        DEFAULT_TIMEOUT_PRESET
    )

    timeout_seconds: int = (
        DEFAULT_TIMEOUT_SECONDS
    )


    # ========================================================
    # LLM Processing
    # ========================================================

    llm_processing_mode: LLMProcessingMode = (
        DEFAULT_LLM_PROCESSING_MODE
    )


    # ========================================================
    # Performance
    # ========================================================

    concurrency_level: ConcurrencyLevel = (
        DEFAULT_CONCURRENCY_LEVEL
    )

    enable_parallel_processing: bool = (
        DEFAULT_ENABLE_PARALLEL_PROCESSING
    )

    max_workers: int = (
        DEFAULT_MAX_WORKERS
    )


    # ========================================================
    # Extraction Options
    # ========================================================

    enable_title_extraction: bool = (
        DEFAULT_ENABLE_TITLE_EXTRACTION
    )

    enable_text_preprocessing: bool = (
        DEFAULT_ENABLE_TEXT_PREPROCESSING
    )

    enable_metadata_extraction: bool = (
        DEFAULT_ENABLE_METADATA_EXTRACTION
    )


    # ========================================================
    # Research Quality Options
    # ========================================================

    include_research_gap: bool = (
        DEFAULT_INCLUDE_RESEARCH_GAP
    )

    include_methodology_analysis: bool = (
        DEFAULT_INCLUDE_METHODOLOGY_ANALYSIS
    )

    include_limitations: bool = (
        DEFAULT_INCLUDE_LIMITATIONS
    )

    include_future_work: bool = (
        DEFAULT_INCLUDE_FUTURE_WORK
    )

    include_citation_analysis: bool = (
        DEFAULT_INCLUDE_CITATION_ANALYSIS
    )


    # ========================================================
    # Debug Options
    # ========================================================

    enable_pipeline_logging: bool = (
        DEFAULT_ENABLE_PIPELINE_LOGGING
    )

    verbose_errors: bool = (
        DEFAULT_VERBOSE_ERRORS
    )


    # ========================================================
    # Internal State
    # ========================================================

    _dirty: bool = field(
        default=False,
        init=False,
        repr=False,
    )


    _saved_snapshot: dict[str, Any] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )


    # ========================================================
    # Factory
    # ========================================================

    @classmethod
    def load_defaults(
        cls,
    ) -> "PipelineSettingsState":
        """
        Create state using default values.
        """

        instance = cls()

        instance.mark_saved()

        return instance


    # ========================================================
    # Update
    # ========================================================

    def update(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Update state value.
        """

        if not hasattr(
            self,
            key,
        ):
            raise AttributeError(
                f"Unknown setting: {key}"
            )


        setattr(
            self,
            key,
            value,
        )


        self._dirty = True


    # ========================================================
    # Validation
    # ========================================================

    def validate(
        self,
    ) -> tuple[bool, list[str]]:
        """
        Validate current configuration.
        """

        return validate_pipeline_settings(
            self.export_json_ready()
        )


    # ========================================================
    # Reset
    # ========================================================

    def reset(
        self,
    ) -> None:
        """
        Restore default configuration.
        """

        default = (
            self.load_defaults()
        )


        for key, value in (
            default.__dict__.items()
        ):

            if key.startswith("_"):
                continue


            setattr(
                self,
                key,
                value,
            )


        self._dirty = True


    # ========================================================
    # Dirty Tracking
    # ========================================================

    def is_dirty(
        self,
    ) -> bool:
        """
        Check unsaved changes.
        """

        return self._dirty


    def mark_saved(
        self,
    ) -> None:
        """
        Mark current state as saved.
        """

        self._saved_snapshot = (
            self.export_json_ready()
        )

        self._dirty = False


    # ========================================================
    # Serialization
    # ========================================================

    def export_json_ready(
        self,
    ) -> dict[str, Any]:
        """
        Export configuration.

        Converts enums into strings.
        """

        data = {}

        for key, value in asdict(self).items():

            if key.startswith("_"):
                continue


            if isinstance(
                value,
                dict,
            ):

                data[key] = {
                    (
                        k.value
                        if hasattr(k, "value")
                        else k
                    ):
                        v
                    for k, v in value.items()
                }


            elif hasattr(
                value,
                "value",
            ):

                data[key] = value.value


            else:

                data[key] = value


        return data


__all__ = [
    "PipelineSettingsState",
]