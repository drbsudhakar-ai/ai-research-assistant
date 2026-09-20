"""
===============================================================================
Project      : AI Research Assistant
Module       : Context Builder
File         : context_builder.py
Version      : 1.0.0

Description:
    Builds the analysis context from a prepared research paper.

Responsibilities:
    - Convert PreparedPaper into PDFExtractionResult.
    - Encapsulate context construction logic.
===============================================================================
"""

from __future__ import annotations

from app.models import PreparedPaper
from app.utils.pdf_extractor import PDFExtractionResult

__all__ = [
    "ContextBuilder",
]


class ContextBuilder:
    """
    Builds the AI analysis context.
    """

    def build(
        self,
        paper: PreparedPaper,
    ) -> PDFExtractionResult:
        """
        Build a PDFExtractionResult from a PreparedPaper.
        """

        return PDFExtractionResult(
            title=paper.title,
            title_source=paper.title_source,
            title_confidence=paper.title_confidence,
            text=paper.text,
            total_pages=paper.total_pages,
            total_characters=paper.total_characters,
        )