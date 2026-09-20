"""
===============================================================================
Project      : AI Research Assistant
Module       : Prepare Paper Pipeline Step
File         : prepare_paper_step.py
Version      : 1.0.0

Description:
    Prepares research paper data for AI analysis.

    Responsibilities:
        - PDF extraction
        - Text preprocessing
        - Metadata preparation
        - Section extraction integration

===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.core.pipeline.base_pipeline_step import (
    BasePipelineStep,
)
from app.core.pipeline.pipeline_context import (
    PipelineContext,
)
from app.core.pipeline.pipeline_keys import PipelineKeys
from app.utils.paper_preprocessor import PaperPreprocessor
from app.utils.pdf_extractor import PDFExtractor

__all__ = [
    "PreparePaperStep",
]


class PreparePaperStep(BasePipelineStep):
    """
    Pipeline step responsible for preparing research paper data.
    """


    VERSION = "1.0.0"


    def __init__(
        self,
        extractor: PDFExtractor,
        preprocessor: PaperPreprocessor,
    ) -> None:
        """
        Initialize prepare paper step.

        Parameters
        ----------
        extractor:
            PDF extraction service.

        preprocessor:
            Paper preprocessing service.
        """

        self._extractor = extractor

        self._preprocessor = preprocessor



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

        return "Prepare Research Paper"



    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Extract and prepare paper content.

        Parameters
        ----------
        context:
            Shared pipeline execution context.
        """


        pdf_path = context.get(PipelineKeys.PDF_PATH)

        if pdf_path is None:
            raise ValueError(
                "PDF path missing from pipeline context"
            )

        pdf_path = Path(pdf_path)

        with pdf_path.open("rb") as pdf_file:
            extraction_result = self._extractor.extract_text(pdf_file)


        if extraction_result is None:

            raise RuntimeError(
                "PDF extraction failed"
            )


        #
        # Prepare structured paper
        #
        prepared_paper = self._preprocessor.prepare(
            extracted=extraction_result,
            filename=pdf_path.name,
        )


        if prepared_paper is None:

            raise RuntimeError(
                "Paper preprocessing failed"
            )

        context.set(PipelineKeys.PDF_RESULT, extraction_result)
        context.set(PipelineKeys.PREPARED_PAPER, prepared_paper)
        context.set(
            PipelineKeys.PAPER_METADATA,
            self._build_metadata(prepared_paper),
        )

        self._report_progress(
            context,
            "Research paper preparation completed",
        )



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_metadata(
        self,
        prepared_paper: Any,
    ) -> dict[str, Any]:
        """
        Create normalized paper metadata.
        """

        return {
            "title": getattr(prepared_paper, "title", None),
            "filename": getattr(prepared_paper, "filename", ""),
            "pages": getattr(prepared_paper, "total_pages", 0),
            "characters": getattr(prepared_paper, "total_characters", 0),
            "title_source": getattr(prepared_paper, "title_source", None),
            "title_confidence": getattr(
                prepared_paper,
                "title_confidence",
                None,
            ),
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