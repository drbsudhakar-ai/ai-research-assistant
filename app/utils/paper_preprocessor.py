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

from dataclasses import dataclass

from app.utils.pdf_extractor import PDFExtractor
from app.utils.pdf_validator import PDFValidator

from streamlit.runtime.uploaded_file_manager import UploadedFile

__all__ = [
    "PaperContent",
    "PaperPreprocessor",
]


@dataclass(slots=True)
class PaperContent:
    """
    Structured paper information.
    """

    title: str
    filename: str
    text: str
    total_pages: int
    total_characters: int


class PaperPreprocessor:
    """
    Coordinates PDF validation and extraction.
    """

    def __init__(self) -> None:
        """
        Initialize PDF preprocessing utilities.
        """

        self._validator = PDFValidator()
        self._extractor = PDFExtractor()

    def prepare(
        self,
        uploaded_file: UploadedFile,
    ) -> PaperContent:
        """
            Validate the uploaded PDF, extract its contents,
            and return structured paper information.
        """
        self._validator.validate(uploaded_file)

        extracted = self._extractor.extract_text(
            uploaded_file
        )

        return PaperContent(
            title=extracted.title,
            filename=uploaded_file.name,
            text=extracted.text,
            total_pages=extracted.total_pages,
            total_characters=extracted.total_characters,
        )