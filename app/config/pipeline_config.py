# =============================================================================
# File: app/config/pipeline_config.py
# Production Ready Pipeline Configuration Layer
# Version: 1.0.0
# =============================================================================

from __future__ import annotations


from dataclasses import (
    dataclass,
    field,
    asdict,
)


from typing import (
    Any,
)


import logging


logger = logging.getLogger(
    __name__
)



# =============================================================================
# Pipeline Stage Configuration
# =============================================================================


@dataclass
class PipelineStageConfig:
    """
    Defines one pipeline stage.

    Example:

        validate_pdf
        prepare_paper
        analyze_paper
        save_history
    """

    name: str

    enabled: bool = True

    order: int = 0

    timeout_seconds: int = 300

    retry_count: int = 1

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    def validate(
        self,
    ) -> tuple[bool, str]:
        """
        Validate stage configuration.
        """

        if not self.name:

            return (
                False,
                "Stage name is required.",
            )


        if self.order < 0:

            return (
                False,
                "Stage order cannot be negative.",
            )


        if self.timeout_seconds <= 0:

            return (
                False,
                "Timeout must be positive.",
            )


        if self.retry_count < 0:

            return (
                False,
                "Retry count cannot be negative.",
            )


        return (
            True,
            "Stage configuration valid.",
        )



# =============================================================================
# Retry Configuration
# =============================================================================


@dataclass
class RetryPolicy:
    """
    Pipeline retry behaviour.
    """

    enabled: bool = True

    max_attempts: int = 3

    delay_seconds: float = 2.0

    exponential_backoff: bool = True



    def validate(
        self,
    ) -> tuple[bool, str]:

        if self.max_attempts <= 0:

            return (
                False,
                "Max attempts must be positive.",
            )


        if self.delay_seconds < 0:

            return (
                False,
                "Delay cannot be negative.",
            )


        return (
            True,
            "Retry policy valid.",
        )



# =============================================================================
# Progress Configuration
# =============================================================================


@dataclass
class PipelineProgressConfig:
    """
    Progress reporting settings.

    Used by:

        ProgressManager
        ProgressRenderer
    """

    enabled: bool = True

    show_percentage: bool = True

    show_stage_name: bool = True

    allow_cancellation: bool = True

    update_interval_ms: int = 500



# =============================================================================
# Resource Configuration
# =============================================================================


@dataclass
class PipelineResourceConfig:
    """
    Runtime resource limits.
    """

    max_pdf_pages: int = 200

    max_text_length: int = 1000000

    max_execution_seconds: int = 1800

    memory_limit_mb: int = 4096



# =============================================================================
# Export Configuration
# =============================================================================


@dataclass
class PipelineExportConfig:
    """
    Analysis output configuration.
    """

    enable_pdf: bool = True

    enable_markdown: bool = True

    enable_docx: bool = True

    enable_html: bool = True

    include_metadata: bool = True

    include_citations: bool = True



# =============================================================================
# Main Pipeline Configuration
# =============================================================================


@dataclass
class PipelineConfig:
    """
    Complete analysis pipeline configuration.
    """


    name: str = (
        "research_analysis_pipeline"
    )


    version: str = (
        "1.0"
    )


    execution_mode: str = (
        "sequential"
    )


    stages: list[PipelineStageConfig] = field(

        default_factory=list

    )


    retry_policy: RetryPolicy = field(

        default_factory=RetryPolicy

    )


    progress: PipelineProgressConfig = field(

        default_factory=PipelineProgressConfig

    )


    resources: PipelineResourceConfig = field(

        default_factory=PipelineResourceConfig

    )


    export: PipelineExportConfig = field(

        default_factory=PipelineExportConfig

    )



    def validate(
        self,
    ) -> tuple[bool, list[str]]:
        """
        Validate pipeline configuration.
        """

        errors = []


        if not self.name:

            errors.append(
                "Pipeline name missing."
            )


        if self.execution_mode not in (

            "sequential",

            "parallel",

        ):

            errors.append(
                "Invalid execution mode."
            )


        for stage in self.stages:

            valid, message = (
                stage.validate()
            )


            if not valid:

                errors.append(
                    message
                )


        valid, message = (
            self.retry_policy.validate()
        )


        if not valid:

            errors.append(
                message
            )


        return (

            len(errors) == 0,

            errors,

        )



    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Export configuration.
        """

        return asdict(
            self
        )



# =============================================================================
# Default Research Pipeline
# =============================================================================


def create_default_pipeline_config(
) -> PipelineConfig:
    """
    Create default research analysis pipeline.
    """

    return PipelineConfig(

        stages=[

            PipelineStageConfig(

                name="validate_pdf",

                order=1,

                timeout_seconds=60,

            ),


            PipelineStageConfig(

                name="prepare_paper",

                order=2,

                timeout_seconds=120,

            ),


            PipelineStageConfig(

                name="analyze_paper",

                order=3,

                timeout_seconds=1200,

                retry_count=2,

            ),


            PipelineStageConfig(

                name="save_history",

                order=4,

                timeout_seconds=60,

            ),

        ]

    )



# =============================================================================
# Global Default Instance
# =============================================================================


DEFAULT_PIPELINE_CONFIG = (
    create_default_pipeline_config()
)



__all__ = [

    "PipelineStageConfig",

    "RetryPolicy",

    "PipelineProgressConfig",

    "PipelineResourceConfig",

    "PipelineExportConfig",

    "PipelineConfig",

    "DEFAULT_PIPELINE_CONFIG",

    "create_default_pipeline_config",

]