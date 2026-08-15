"""
===============================================================================
Project      : AI Research Assistant
Module       : Service Container
File         : service_container.py
Version      : 1.0.0

Description:
    Application dependency container.

    Responsible for creating and exposing application services.

    This module acts as the composition root for dependency injection.

===============================================================================
"""

from __future__ import annotations

from functools import cached_property


from app.utils.pdf_extractor import (
    PDFExtractor,
)

from app.utils.paper_preprocessor import (
    PaperPreprocessor,
)

from app.agents.paper_analyzer import (
    PaperAnalyzer,
)

from app.services.history_service import (
    HistoryService,
)


from app.core.pipeline.research_analysis_pipeline_factory import (
    ResearchAnalysisPipelineFactory,
)


from app.services.analysis_service import (
    AnalysisService,
)


__all__ = [
    "ServiceContainer",
]



class ServiceContainer:
    """
    Central dependency container.

    All application services are created here.
    """


    VERSION = "1.0.0"



    # ------------------------------------------------------------------
    # PDF Services
    # ------------------------------------------------------------------

    @cached_property
    def pdf_extractor(
        self,
    ) -> PDFExtractor:
        """
        PDF extraction service.
        """

        return PDFExtractor()



    @cached_property
    def paper_preprocessor(
        self,
    ) -> PaperPreprocessor:
        """
        Paper preprocessing service.
        """

        return PaperPreprocessor()



    # ------------------------------------------------------------------
    # AI Services
    # ------------------------------------------------------------------

    @cached_property
    def paper_analyzer(
        self,
    ) -> PaperAnalyzer:
        """
        AI paper analysis service.
        """

        return PaperAnalyzer()



    # ------------------------------------------------------------------
    # Persistence Services
    # ------------------------------------------------------------------

    @cached_property
    def history_service(
        self,
    ) -> HistoryService:
        """
        Analysis history service.
        """

        return HistoryService()



    # ------------------------------------------------------------------
    # Pipeline Services
    # ------------------------------------------------------------------

    @cached_property
    def research_analysis_pipeline_factory(
        self,
    ) -> ResearchAnalysisPipelineFactory:
        """
        Research pipeline factory.
        """

        return ResearchAnalysisPipelineFactory(

            pdf_extractor=self.pdf_extractor,

            paper_preprocessor=self.paper_preprocessor,

            paper_analyzer=self.paper_analyzer,

            history_service=self.history_service,

        )



    # ------------------------------------------------------------------
    # Application Services
    # ------------------------------------------------------------------

    @cached_property
    def analysis_service(
        self,
    ) -> AnalysisService:
        """
        Main analysis orchestration service.
        """

        return AnalysisService(

            pipeline_factory=(
                self.research_analysis_pipeline_factory
            )

        )



    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Container name.
        """

        return "Application Service Container"



    @property
    def version(
        self,
    ) -> str:
        """
        Container version.
        """

        return self.VERSION