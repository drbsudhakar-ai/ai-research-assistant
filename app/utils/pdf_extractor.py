"""
===============================================================================
Project      : AI Research Assistant
Module       : PDF Utilities
File         : pdf_extractor.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
    Utility module for extracting text and metadata from PDF documents.

Responsibilities:
    - Validate PDF documents.
    - Extract text page by page.
    - Return extraction statistics.

Notes:
    - This module contains no Streamlit code.
    - This module contains no AI logic.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO
from app.utils.title_extractor import TitleExtractor
import fitz


__all__ = [
    "PDFExtractionResult",
    "PDFExtractor",
]


# =============================================================================
# Data Models
# =============================================================================


@dataclass(slots=True, frozen=True)
class PDFExtractionResult:
    title: str
    title_source: str
    title_confidence: float
    text: str
    total_pages: int
    total_characters: int


# =============================================================================
# PDF Extractor
# =============================================================================


class PDFExtractor:
    """
    Utility class for extracting information from PDF documents.
    """


    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @staticmethod
    def extract_text(
        file: BinaryIO,
    ) -> PDFExtractionResult:
        """
        Extract text and metadata from a PDF.

        Parameters
        ----------
        file : BinaryIO
            PDF file.

        Returns
        -------
        PDFExtractionResult

        Raises
        ------
        ValueError
            If the PDF is invalid or contains no extractable text.
        """

        try:
            
            file.seek(0)

            pdf_bytes = file.read()

            with fitz.open(
                stream=pdf_bytes,
                filetype="pdf",
            ) as document:

                extracted_pages = [
                    page.get_text("text").strip()
                    for page in document
                ]

                extracted_text = "\n".join(
                    page
                    for page in extracted_pages
                    if page
                ).strip()

                if not extracted_text:
                    raise ValueError(
                        "The PDF contains no extractable text."
                    )

                title_result = TitleExtractor.extract(document)
                title = title_result.title
                source = title_result.source
                confidence = title_result.confidence

                return PDFExtractionResult(
                    title=title,
                    title_source=source,
                    title_confidence=confidence,
                    text=extracted_text,
                    total_pages=len(document),
                    total_characters=len(extracted_text),
                )

        except (fitz.FileDataError, RuntimeError) as exc:
            raise ValueError(
                "Invalid or corrupted PDF document."
            ) from exc