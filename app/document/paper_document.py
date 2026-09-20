"""
===============================================================================
Project      : AI Research Assistant
Module       : Document Model
File         : paper_document.py
Version      : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .paper_metadata import PaperMetadata
from .paper_section import PaperSection
from .processing_info import ProcessingInfo
from .validation_result import ValidationResult


@dataclass(frozen=True, slots=True)
class PaperDocument:
    """
    Canonical representation of a processed research paper.

    Every component of the application should consume this object
    instead of raw extracted text.
    """

    metadata: PaperMetadata

    raw_text: str

    cleaned_text: str

    research_text: str

    sections: list[PaperSection] = field(default_factory=list)

    references: str = ""

    appendix: str = ""

    acknowledgements: str = ""

    validation: ValidationResult = field(
        default_factory=ValidationResult
    )

    processing: ProcessingInfo = field(
        default_factory=ProcessingInfo
    )

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def research_character_count(self) -> int:
        return len(self.research_text)

    @property
    def is_valid(self) -> bool:
        return self.validation.valid