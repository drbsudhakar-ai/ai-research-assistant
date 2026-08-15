"""
===============================================================================
Project      : AI Research Assistant
Module       : Paper Analyzer
File         : app/agents/paper_analyzer.py
Version      : 3.0.0
Author       : Dr. B. Sudhakar

Description:
    Orchestrates AI analysis of a prepared research paper.

Responsibilities:
    - Validate prepared paper.
    - Build analysis prompt.
    - Invoke configured LLM service.
    - Report progress.
    - Validate AI response.
    - Produce AnalysisResult.

Non-Responsibilities:
    - PDF extraction.
    - Database persistence.
    - UI rendering.
===============================================================================
"""

from __future__ import annotations

import logging
from time import perf_counter
from typing import Final

from app.core.progress.progress_reporter import ProgressReporter
from app.core.progress.progress_stage import ProgressStage
from app.models.analysis_result import AnalysisResult
from app.models.prepared_paper import PreparedPaper
from app.prompts.common.system_prompt import SYSTEM_PROMPT
from app.prompts.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService

__all__ = [
    "PaperAnalyzer",
]

_LOGGER = logging.getLogger(__name__)


# =============================================================================
# Progress
# =============================================================================

class AnalysisProgress:
    """
    Progress percentages.
    """

    def __new__(cls) -> None:
        raise TypeError(
            "AnalysisProgress cannot be instantiated."
        )

    VALIDATE: Final[int] = 45
    CHECK_SERVICE: Final[int] = 50
    BUILD_PROMPT: Final[int] = 55
    GENERATE: Final[int] = 70
    VALIDATE_RESPONSE: Final[int] = 88
    CREATE_RESULT: Final[int] = 95


# =============================================================================
# Paper Analyzer
# =============================================================================

class PaperAnalyzer:
    """
    Performs AI analysis of a prepared research paper.
    """

    _MIN_TEXT_LENGTH: Final[int] = 200
    _MIN_RESPONSE_LENGTH: Final[int] = 100

    def __init__(
        self,
        llm_service: LLMService | None = None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:

        self._llm = llm_service or LLMService()
        self._prompt_builder = (
            prompt_builder
            or PromptBuilder()
        )

    # =========================================================================
    # Progress
    # =========================================================================
    def _report(
        self,
        reporter: ProgressReporter | None,
        *,
        stage: ProgressStage,
        message: str,
        percentage: int,
    ) -> None:
        """
        Publish progress update.
        """

        if reporter is None:
            return

        reporter.update(
            message=message,
            percentage=percentage,
            stage=stage,
        )


    def _report_analysis(
        self,
        reporter: ProgressReporter | None,
        *,
        message: str,
        percentage: int,
    ) -> None:

        self._report(
            reporter,
            stage=ProgressStage.ANALYZING,
            message=message,
            percentage=percentage,
        )

    # =========================================================================
    # Validation
    # =========================================================================

    def _validate_paper(
        self,
        paper: PreparedPaper,
    ) -> None:
        """
        Validate prepared paper.
        """

        if paper is None:
            raise ValueError(
                "paper cannot be None."
            )

        if not paper.text.strip():
            raise ValueError(
                "Paper text is empty."
            )

        if len(
            paper.text.strip()
        ) < self._MIN_TEXT_LENGTH:

            raise ValueError(
                "Extracted paper text is too short."
            )

    def _validate_response(
        self,
        content: str,
    ) -> None:
        """
        Validate AI response.
        """

        if not content.strip():
            raise RuntimeError(
                "LLM returned an empty response."
            )

        if len(
            content.strip()
        ) < self._MIN_RESPONSE_LENGTH:

            raise RuntimeError(
                "LLM response is too short."
            )

    # =========================================================================
    # Public API
    # =========================================================================

    def analyze(
        self,
        paper: PreparedPaper,
        progress_reporter: ProgressReporter | None = None,
    ) -> AnalysisResult:
        """
        Analyze a prepared research paper.

        Parameters
        ----------
        paper:
            Prepared research paper.

        progress_reporter:
            Optional progress reporter.

        Returns
        -------
        AnalysisResult
            Canonical analysis outcome. Persistence uses AnalysisRecord.
        """

        start_time = perf_counter()

        self._report_analysis(
            progress_reporter,
            message="Validating research paper...",
            percentage=AnalysisProgress.VALIDATE,
        )

        self._validate_paper(paper)

        self._report_analysis(
            progress_reporter,
            message="Checking AI provider...",
            percentage=AnalysisProgress.CHECK_SERVICE,
        )

        if not self._llm.is_available():
            raise RuntimeError(
                f"{self._llm.provider} service is unavailable."
            )

        self._report_analysis(
            progress_reporter,
            message="Building analysis prompt...",
            percentage=AnalysisProgress.BUILD_PROMPT,
        )
        
        
        print(">>> Building prompt")
        user_prompt = self._prompt_builder.build(
            paper
        )
        print(">>> Prompt size:", len(user_prompt))
        
        self._report_analysis(
            progress_reporter,
            message="Analyzing research paper...",
            percentage=AnalysisProgress.GENERATE,
        )

        _LOGGER.info(
            "Starting AI analysis using provider='%s', model='%s'.",
            self._llm.provider,
            self._llm.model,
        )

        print(">>> Calling Ollama")
        response = self._llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        print(">>> Ollama returned")
        self._report_analysis(
            progress_reporter,
            message="Validating AI response...",
            percentage=AnalysisProgress.VALIDATE_RESPONSE,
        )

        self._validate_response(
            response.content
        )

        execution_time = (
            perf_counter() - start_time
        )

        self._report_analysis(
            progress_reporter,
            message="Creating analysis result...",
            percentage=AnalysisProgress.CREATE_RESULT,
        )

        result = AnalysisResult.from_llm_response(
            response,
            execution_time=execution_time,
        )

        _LOGGER.info(
            "Analysis completed successfully in %.2f seconds.",
            execution_time,
        )

        return result

    # =========================================================================
    # Information
    # =========================================================================

    @property
    def provider(self) -> str:
        """
        Return the configured AI provider.
        """

        return self._llm.provider

    @property
    def model(self) -> str:
        """
        Return the configured AI model.
        """

        return self._llm.model

    # =========================================================================
    # Health
    # =========================================================================

    def is_available(self) -> bool:
        """
        Determine whether the configured LLM provider is available.

        Returns
        -------
        bool
        """

        return self._llm.is_available()

    # =========================================================================
    # Prompt
    # =========================================================================

    def build_prompt(
        self,
        paper: PreparedPaper,
    ) -> str:
        """
        Build the analysis prompt.

        This method exists primarily for testing and future extensibility.

        Parameters
        ----------
        paper:
            Prepared research paper.

        Returns
        -------
        str
        """

        self._validate_paper(paper)

        return self._prompt_builder.build(
            paper,
        )

    # =========================================================================
    # Representation
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return a developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"provider={self.provider!r}, "
            f"model={self.model!r})"
        )