"""
===============================================================================
Project      : AI Research Assistant
Module       : Research Analysis Pipeline Factory
File         : research_analysis_pipeline_factory.py
Version      : 1.0.0

Description:
    Factory responsible for creating configured research analysis pipelines.

    This module wires application services with pipeline steps.

===============================================================================
"""

from __future__ import annotations

from app.core.pipeline.research_analysis_pipeline import (
    ResearchAnalysisPipeline,
)

from app.utils.pdf_extractor import PDFExtractor
from app.utils.paper_preprocessor import PaperPreprocessor
from app.agents.paper_analyzer import PaperAnalyzer
from app.services.history_service import HistoryService


__all__ = [
    "ResearchAnalysisPipelineFactory",
]


class ResearchAnalysisPipelineFactory:
    """
    Creates configured research analysis pipelines.

    The factory owns dependency wiring.
    """

    VERSION = "1.0.0"


    def __init__(
        self,
        pdf_extractor: PDFExtractor,
        paper_preprocessor: PaperPreprocessor,
        paper_analyzer: PaperAnalyzer,
        history_service: HistoryService,
    ) -> None:
        """
        Initialize factory dependencies.

        Parameters
        ----------
        pdf_extractor:
            PDF extraction service.

        paper_preprocessor:
            Paper preparation service.

        paper_analyzer:
            AI analysis service.

        history_service:
            Analysis history persistence service.
        """

        self._pdf_extractor = pdf_extractor
        self._paper_preprocessor = paper_preprocessor
        self._paper_analyzer = paper_analyzer
        self._history_service = history_service


    # ------------------------------------------------------------------
    # Factory API
    # ------------------------------------------------------------------

    def create(
        self,
    ) -> ResearchAnalysisPipeline:
        """
        Create configured research analysis pipeline.

        Returns
        -------
        ResearchAnalysisPipeline
            Ready-to-run pipeline.
        """

        from app.pipeline.steps.validate_pdf_step import (
            ValidatePdfStep,
        )

        from app.pipeline.steps.prepare_paper_step import (
            PreparePaperStep,
        )

        from app.pipeline.steps.analyze_paper_step import (
            AnalyzePaperStep,
        )

        from app.pipeline.steps.save_history_step import (
            SaveHistoryStep,
        )


        steps = [

            ValidatePdfStep(),

            PreparePaperStep(
                extractor=self._pdf_extractor,
                preprocessor=self._paper_preprocessor,
            ),

            AnalyzePaperStep(
                analyzer=self._paper_analyzer,
            ),

            SaveHistoryStep(
                history_service=self._history_service,
            ),
        ]


        return ResearchAnalysisPipeline(
            steps=steps,
        )


    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Factory name.
        """

        return "Research Analysis Pipeline Factory"


    @property
    def version(
        self,
    ) -> str:
        """
        Factory version.
        """

        return self.VERSION