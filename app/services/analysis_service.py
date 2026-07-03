"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Service
File         : analysis_service.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Application service that coordinates the complete research paper
analysis workflow.

Responsibilities:
    - Prepare uploaded research papers.
    - Invoke the AI paper analyzer.
    - Return the completed analysis record.

Future Responsibilities:
    - Persist analysis history.
    - Generate reports.
    - Notify other services if required.

This module contains application orchestration logic only.
===============================================================================
"""

from __future__ import annotations
from app.services.history_service import HistoryService
from app.agents.paper_analyzer import PaperAnalyzer
from app.models.analysis_record import AnalysisRecord
from app.utils.paper_preprocessor import (
    PaperPreprocessor,
)
from app.utils.pdf_extractor import PDFExtractionResult

__all__ = [
    "AnalysisService",
]


class AnalysisService:
    """
    Coordinates the complete paper analysis workflow.
    """

    def __init__(
        self,
        preprocessor: PaperPreprocessor | None = None,
        analyzer: PaperAnalyzer | None = None,
        history_service: HistoryService | None = None,
    ) -> None:
        """
        Initialize the analysis service.
        """

        self._preprocessor = (
            preprocessor or PaperPreprocessor()
        )

        self._analyzer = (
            analyzer or PaperAnalyzer()
        )

        self._history_service = (
            history_service or HistoryService()
        )

    def analyze(
        self,
        uploaded_file,
    ) -> AnalysisRecord:
        """
        Analyze an uploaded research paper.

        Parameters
        ----------
        uploaded_file
            Streamlit uploaded PDF file.

        Returns
        -------
        AnalysisRecord
            Completed analysis record.

        Raises
        ------
        ValueError
            If the uploaded PDF is invalid.

        RuntimeError
            If the AI analysis fails.
        """

        paper = self._preprocessor.prepare(
            uploaded_file
        )

        pdf_result = PDFExtractionResult(
            title=paper.title,
            text=paper.text,
            total_pages=paper.total_pages,
            total_characters=paper.total_characters,
        )

        record = self._analyzer.analyze(
            pdf_result=pdf_result,
            filename=paper.filename,
        )

        # Automatically save analysis history
        self._history_service.save_analysis(record)

        return record