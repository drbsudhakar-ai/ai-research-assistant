"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Paper Pipeline Step
File         : analyze_paper_step.py
Version      : 1.0.0

Description:
    Executes AI-powered research paper analysis.

    Responsibilities:
        - Consume prepared paper data
        - Invoke PaperAnalyzer agent
        - Store analysis result
        - Preserve execution metadata

===============================================================================
"""

from __future__ import annotations

from time import perf_counter
from typing import Any


from app.core.pipeline.base_pipeline_step import (
    BasePipelineStep,
)

from app.core.pipeline.pipeline_context import (
    PipelineContext,
)


from app.agents.paper_analyzer import PaperAnalyzer


__all__ = [
    "AnalyzePaperStep",
]


class AnalyzePaperStep(BasePipelineStep):
    """
    Pipeline step responsible for AI analysis.
    """


    VERSION = "1.0.0"


    def __init__(
        self,
        analyzer: PaperAnalyzer,
    ) -> None:
        """
        Initialize analysis step.

        Parameters
        ----------
        analyzer:
            Research paper analysis agent.
        """

        self._analyzer = analyzer



    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Step name.
        """

        return "Analyze Research Paper"



    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execute AI analysis.

        Parameters
        ----------
        context:
            Shared pipeline execution context.
        """
        # progress_reporter = context.progress_reporter
        prepared_paper = context.get("prepared_paper")

        if prepared_paper is None:
            raise ValueError("Prepared paper not available")

        self._report_progress(
            context,
            "Starting AI analysis...",
        )

        start_time = perf_counter()

        analysis_result = (
            self._analyzer.analyze(
                paper=prepared_paper,
                progress_reporter=context.progress_reporter,
            )
        )

        execution_time = (
            perf_counter() - start_time
        )


        if analysis_result is None:

            raise RuntimeError(
                "Paper analysis failed"
            )


        #
        # Store result
        #
        context.set(
            "analysis_result",
            analysis_result,
        )

        context.set(
            "analysis_metadata",
            self._build_metadata(
                analysis_result,
                execution_time,
            ),
        )


        self._report_progress(
            context,
            "AI paper analysis completed",
        )



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_metadata(
        self,
        analysis_result: Any,
        execution_time: float,
    ) -> dict[str, Any]:
        """
        Build analysis metadata.
        """

        return {

            "execution_time": round(
                execution_time,
                2,
            ),

            "provider": getattr(
                analysis_result,
                "provider",
                None,
            ),

            "model": getattr(
                analysis_result,
                "model",
                None,
            ),

            "status": "completed",

        }



    def _report_progress(
        self,
        context: PipelineContext,
        message: str,
    ) -> None:
        """
        Notify optional progress reporter.
        """

        reporter = getattr(
            context,
            "progress_reporter",
            None,
        )


        if reporter is None:
            return


        reporter.update(
            message=message,
        )