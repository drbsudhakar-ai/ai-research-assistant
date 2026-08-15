"""
===============================================================================
Project      : AI Research Assistant
Module       : Paper Analyzer
File         : paper_preprocessor.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Prepare uploaded research papers for AI analysis.

Responsibilities:
    - Validate uploaded PDF.
    - Extract paper contents.
    - Return structured paper information.

Business logic related to AI must not be implemented here.
===============================================================================
"""

from __future__ import annotations

from app.services.paper_section_extractor import PaperSectionExtractor
from app.models import PreparedPaper
from app.utils.pdf_extractor import PDFExtractionResult

__all__ = [
    
    "PaperPreprocessor",
]

class PaperPreprocessor:
    """
    Builds a PreparedPaper from extracted PDF content.
    """

    def __init__(self) -> None:
        """
        Initialize paper preprocessing utilities.
        """

        # self._validator = PDFValidator()
        # self._extractor = PDFExtractor()
        self._section_extractor = PaperSectionExtractor()

    def prepare(
        self,
        extracted: PDFExtractionResult,
        filename: str,
    ) -> PreparedPaper:
        """
            Validate the uploaded PDF, extract its contents,
            and return structured paper information.
        """
        
        if extracted is None:
            raise ValueError(
                "Extraction result cannot be None."
            )
        
        paper_sections = self._section_extractor.extract(
            title=extracted.title,
            text=extracted.text,
        )

        prepared = PreparedPaper(
            title=extracted.title,
            title_source=extracted.title_source,
            title_confidence=extracted.title_confidence,
            filename=filename,
            text=extracted.text,
            total_pages=extracted.total_pages,
            total_characters=extracted.total_characters,
            sections=paper_sections,
        )

        return prepared