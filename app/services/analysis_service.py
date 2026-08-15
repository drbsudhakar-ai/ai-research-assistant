"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Service
File         : analysis_service.py
Version      : 3.0.0

Description:
    Application service responsible for executing research paper analysis.

    Responsibilities:
        - Create pipeline execution context
        - Attach progress reporting
        - Handle cancellation
        - Execute research analysis pipeline

===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.core.pipeline.pipeline_context import (
    PipelineContext,
)
from app.core.pipeline.pipeline_keys import PipelineKeys
from app.core.pipeline.pipeline_result import (
    PipelineResult,
)
from app.core.pipeline.pipeline_runner import (
    PipelineRunner,
)
from app.core.pipeline.research_analysis_pipeline_factory import (
    ResearchAnalysisPipelineFactory,
)
from app.core.progress.progress_manager import (
    ProgressManager,
)
from app.core.progress.progress_stage import ProgressStage
from app.models.analysis_result import AnalysisResult

__all__ = [
    "AnalysisService",
]



class AnalysisService:
    """
    Orchestration service for research paper analysis.
    """


    VERSION = "3.0.0"



    def __init__(
        self,
        pipeline_factory: ResearchAnalysisPipelineFactory,
    ) -> None:
        """
        Initialize analysis service.

        Parameters
        ----------
        pipeline_factory:
            Factory creating configured pipelines.
        """

        self._pipeline_factory = pipeline_factory



    # =========================================================================
    # Main API
    # =========================================================================

    def analyze(
        self,
        pdf_path: str | Path,
        metadata: dict[str, Any] | None = None,
        progress_manager: ProgressManager | None = None,
    ) -> PipelineResult:
        """
        Execute research paper analysis.

        Parameters
        ----------
        pdf_path:
            Uploaded PDF path.

        metadata:
            Additional execution metadata.

        progress_manager:
            Optional progress manager used by UI.

        Returns
        -------
        PipelineResult
            Pipeline execution result.
        """


        progress_manager = (
            progress_manager
            or ProgressManager()
        )


        #
        # Create pipeline context
        #
        context = PipelineContext(

            data={

                PipelineKeys.PDF_PATH: str(
                    pdf_path
                ),

                "metadata": (
                    metadata
                    or {}
                ),

            },

            progress_reporter=(
                progress_manager
            ),

            cancellation_token=(

                progress_manager.cancellation_token

            ),

        )


        #
        # Initial progress
        #
        context.report_progress(

            message="Starting analysis",

            percentage=0,

            stage=ProgressStage.STARTING,

        )


        #
        # Create pipeline
        #
        pipeline = (
            self._pipeline_factory.create()
        )


        #
        # Execute pipeline
        #
        runner = PipelineRunner(
            pipeline
        )


        result = runner.run(
            context
        )

        if result.success:

            context.report_progress(

                message="Analysis completed",

                percentage=100,

                stage=ProgressStage.COMPLETED,

            )

        return result

    def result_from_pipeline(self, pipeline_result: PipelineResult) -> AnalysisResult | None:
        """Return the canonical analysis outcome from a pipeline envelope."""

        stored = pipeline_result.context.get(PipelineKeys.ANALYSIS_RESULT)
        if stored is None:
            return None
        if isinstance(stored, AnalysisResult):
            return stored
        raise TypeError(
            "Pipeline analysis_result must be an AnalysisResult."
        )



    # =========================================================================
    # Async API
    # =========================================================================

    async def analyze_async(
        self,
        pdf_path: str | Path,
        metadata: dict[str, Any] | None = None,
        progress_manager: ProgressManager | None = None,
    ) -> PipelineResult:
        """
        Async wrapper.

        Keeps future compatibility for async LLM providers.
        """

        return self.analyze(

            pdf_path=pdf_path,

            metadata=metadata,

            progress_manager=progress_manager,

        )



    # =========================================================================
    # Metadata
    # =========================================================================

    @property
    def name(
        self,
    ) -> str:
        """
        Service name.
        """

        return "Research Analysis Service"



    @property
    def version(
        self,
    ) -> str:
        """
        Service version.
        """

        return self.VERSION