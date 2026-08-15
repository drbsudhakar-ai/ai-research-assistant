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

from dataclasses import asdict, dataclass
from typing import Any

from app.models.exceptions import DomainValidationError
from app.models.paper_sections import PaperSections

__all__ = [
    "PreparedPaper",
]


@dataclass(slots=True, frozen=True)
class PreparedPaper:
    """Prepared research paper ready for AI analysis.

    This is a data contract only. It does not extract PDFs or import Streamlit.
    """

    title: str
    title_source: str
    title_confidence: float
    filename: str
    text: str
    total_pages: int
    total_characters: int
    sections: PaperSections

    def __post_init__(self) -> None:
        if not isinstance(self.title, str):
            raise DomainValidationError("title must be a string.", field="title")
        if not isinstance(self.filename, str):
            raise DomainValidationError("filename must be a string.", field="filename")
        if not isinstance(self.text, str):
            raise DomainValidationError("text must be a string.", field="text")
        if not isinstance(self.sections, PaperSections):
            raise DomainValidationError(
                "sections must be a PaperSections instance.",
                field="sections",
            )
        if self.total_pages < 0:
            raise DomainValidationError(
                "total_pages cannot be negative.",
                field="total_pages",
            )
        if self.total_characters < 0:
            raise DomainValidationError(
                "total_characters cannot be negative.",
                field="total_characters",
            )
        if not 0.0 <= float(self.title_confidence) <= 1.0:
            raise DomainValidationError(
                "title_confidence must be between 0 and 1.",
                field="title_confidence",
            )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["sections"] = self.sections.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PreparedPaper:
        payload = dict(data)
        sections = payload.get("sections", PaperSections())
        if isinstance(sections, dict):
            payload["sections"] = PaperSections.from_dict(sections)
        return cls(**payload)
