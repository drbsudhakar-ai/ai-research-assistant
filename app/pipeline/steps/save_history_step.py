"""
===============================================================================
Project      : AI Research Assistant
Module       : Save History Pipeline Step
File         : save_history_step.py
Version      : 1.0.0

Description:
    Persists completed research analysis results.

    Responsibilities:
        - Create history record
        - Store analysis metadata
        - Save using HistoryService
        - Attach persistence result to pipeline context

===============================================================================
"""

from __future__ import annotations

from typing import Any


from app.core.pipeline.base_pipeline_step import (
    BasePipelineStep,
)

from app.core.pipeline.pipeline_context import (
    PipelineContext,
)


from app.models.analysis_record import AnalysisRecord
from app.services.history_service import (
    HistoryService,
)


__all__ = [
    "SaveHistoryStep",
]


class SaveHistoryStep(BasePipelineStep):
    """
    Pipeline step responsible for analysis persistence.
    """


    VERSION = "1.0.0"


    def __init__(
        self,
        history_service: HistoryService,
    ) -> None:
        """
        Initialize history saving step.

        Parameters
        ----------
        history_service:
            Service responsible for storing analysis history.
        """

        self._history_service = history_service



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

        return "Save Analysis History"



    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Save analysis result.

        Parameters
        ----------
        context:
            Shared pipeline execution context.
        """


        analysis_result = context.data.get(
            "analysis_result"
        )


        if analysis_result is None:

            raise ValueError(
                "Analysis result missing"
            )


        paper_metadata = context.data.get(
            "paper_metadata",
            {},
        )


        analysis_metadata = context.data.get(
            "analysis_metadata",
            {},
        )


        record = self._build_record(
            analysis_result,
            paper_metadata,
            analysis_metadata,
        )

        record_id = self._history_service.save_analysis(record)
        # saved_record = (
        #      self._history_service.save_analysis(
        #         record
        #     )
        # )


        #
        # Store persistence result
        #
        
        context.data["history_record_id"] = record_id
        # context.data["history_record"] = (
        #     saved_record
        # )


        self._report_progress(
            context,
            "Analysis history saved",
        )



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_record(
        self,
        analysis_result: Any,
        paper_metadata: dict[str, Any],
        analysis_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build history persistence payload.
        """

        return AnalysisRecord(
            title=paper_metadata.get("title", "Unknown Paper"),
            filename=paper_metadata.get("filename", ""),
            input_source="PDF",
            analysis_type="Research Paper Analysis",
            total_pages=paper_metadata.get("pages", 0),
            total_characters=paper_metadata.get("characters", 0),
            analysis=analysis_result.analysis,
            provider=analysis_metadata.get("provider", ""),
            model=analysis_metadata.get("model", ""),
            execution_time=analysis_metadata.get("execution_time", 0.0),
        )


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