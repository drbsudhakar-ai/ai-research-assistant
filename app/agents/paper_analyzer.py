"""
===============================================================================
Project      : AI Research Assistant
Module       : Paper Analyzer
File         : paper_analyzer.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
    Orchestrates the research paper analysis workflow.

Responsibilities:
    - Validate extracted paper text.
    - Build analysis prompts.
    - Invoke the configured LLM service.
    - Measure execution time.
    - Produce an AnalysisRecord.

Notes:
    - This module contains orchestration logic only.
    - It does not interact with the UI or the database.
===============================================================================
"""

from __future__ import annotations

import time

from app.models.analysis_record import AnalysisRecord
from app.prompts.common.system_prompt import SYSTEM_PROMPT
from app.prompts.research.paper_analysis_prompt import (
    build_paper_analysis_prompt,
)
from app.services.ollama_service import OllamaService
from app.utils.pdf_extractor import PDFExtractionResult

__all__ = [
    "PaperAnalyzer",
]


class PaperAnalyzer:
    """
    Orchestrates research paper analysis.
    """

    def __init__(
        self,
        llm_service: OllamaService | None = None,
    ) -> None:
        """
        Initialize the paper analyzer.

        Parameters
        ----------
        llm_service : OllamaService | None, optional
            Language model service.
            If omitted, a default OllamaService instance is created.
        """

        self._llm = llm_service or OllamaService()

    def analyze(
        self,
        pdf_result: PDFExtractionResult,
        filename: str,
    ) -> AnalysisRecord:
        """
        Analyze a research paper.

        Parameters
        ----------
        pdf_result : PDFExtractionResult
            Extracted PDF content.

        filename : str
            Original PDF filename.

        Returns
        -------
        AnalysisRecord
            Completed analysis record.

        Raises
        ------
        ValueError
            If the extracted text is empty.

        RuntimeError
            If the Ollama server is unavailable.
        """

        if not pdf_result.text.strip():
            raise ValueError(
                "No text was extracted from the PDF."
            )

        if not self._llm.is_available():
            raise RuntimeError(
                "Ollama server is not available."
            )

        user_prompt = build_paper_analysis_prompt(
            pdf_result.text
        )

        start_time = time.perf_counter()

        response = self._llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        execution_time = (
            time.perf_counter() - start_time
        )

        return AnalysisRecord(
            title=pdf_result.title,
            filename=filename,
            input_source="PDF Upload",
            analysis_type="Research Paper Analysis",

            # -----------------------------------------------------------------
            # PDF Statistics
            # -----------------------------------------------------------------
            total_pages=pdf_result.total_pages,
            total_characters=pdf_result.total_characters,

            # -----------------------------------------------------------------
            # AI Analysis
            # -----------------------------------------------------------------
            analysis=response.content,

            # -----------------------------------------------------------------
            # LLM Information
            # -----------------------------------------------------------------
            provider=response.provider,
            model=response.model,

            # -----------------------------------------------------------------
            # Performance
            # -----------------------------------------------------------------
            execution_time=execution_time,
        )