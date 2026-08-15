"""
===============================================================================
Project      : AI Research Assistant
Module       : Models
File         : prepared_paper.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Immutable model representing a research paper after preprocessing.

Responsibilities:
    - Store validated paper metadata.
    - Store extracted text.
    - Serve as the contract between preprocessing and analysis.

Notes:
    - No business logic.
    - No Streamlit dependency.
    - No database dependency.
===============================================================================
"""

from __future__ import annotations
from app.models.paper_sections import PaperSections

from dataclasses import dataclass


__all__ = [
    "PreparedPaper",
]


@dataclass(slots=True, frozen=True)
class PreparedPaper:
    """
    Fully prepared research paper ready for AI analysis.
    """

    title: str

    title_source: str

    title_confidence: float

    filename: str

    text: str

    total_pages: int

    total_characters: int
    
    sections: PaperSections