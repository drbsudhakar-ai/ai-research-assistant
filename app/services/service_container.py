"""
===============================================================================
Project      : AI Research Assistant
Module       : Service Container
File         : service_container.py
Version      : 1.1.0

Description:
    Application dependency container / composition root.

    Services are constructed from one ApplicationConfig instance.
===============================================================================
"""

from __future__ import annotations

from functools import cached_property

from app.agents.paper_analyzer import PaperAnalyzer
from app.config.application_config import ApplicationConfig
from app.config.loader import get_application_config
from app.core.pipeline.research_analysis_pipeline_factory import (
    ResearchAnalysisPipelineFactory,
)
from app.services.analysis_service import AnalysisService
from app.services.history_service import HistoryService
from app.services.llm_service import LLMService
from app.storage.history_repository import HistoryRepository
from app.utils.paper_preprocessor import PaperPreprocessor
from app.utils.pdf_extractor import PDFExtractor

__all__ = [
    "ServiceContainer",
]


class ServiceContainer:
    """Central dependency container. All application services are created here."""

    VERSION = "1.1.0"

    def __init__(self, config: ApplicationConfig | None = None) -> None:
        self._config = config or get_application_config()

    @property
    def config(self) -> ApplicationConfig:
        """Validated application configuration for this container."""

        return self._config

    @cached_property
    def pdf_extractor(self) -> PDFExtractor:
        return PDFExtractor()

    @cached_property
    def paper_preprocessor(self) -> PaperPreprocessor:
        return PaperPreprocessor()

    @cached_property
    def llm_service(self) -> LLMService:
        return LLMService.from_config(self._config)

    @cached_property
    def paper_analyzer(self) -> PaperAnalyzer:
        return PaperAnalyzer(llm_service=self.llm_service)

    @cached_property
    def history_repository(self) -> HistoryRepository:
        return HistoryRepository()

    @cached_property
    def history_service(self) -> HistoryService:
        return HistoryService(repository=self.history_repository)

    @cached_property
    def research_analysis_pipeline_factory(self) -> ResearchAnalysisPipelineFactory:
        return ResearchAnalysisPipelineFactory(
            pdf_extractor=self.pdf_extractor,
            paper_preprocessor=self.paper_preprocessor,
            paper_analyzer=self.paper_analyzer,
            history_service=self.history_service,
        )

    @cached_property
    def analysis_service(self) -> AnalysisService:
        return AnalysisService(pipeline_factory=self.research_analysis_pipeline_factory)

    @property
    def name(self) -> str:
        return "Application Service Container"

    @property
    def version(self) -> str:
        return self.VERSION
