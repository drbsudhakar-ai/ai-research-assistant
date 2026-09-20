"""
===============================================================================
Project      : AI Research Assistant
Module       : Document Model
File         : paper_section.py
Version      : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PaperSection:
    """
    Represents one logical section of a research paper.
    """

    name: str

    heading: str

    content: str

    start_index: int

    end_index: int

    page_number: int | None = None

    confidence: float = 1.0

    @property
    def character_count(self) -> int:
        return len(self.content)

    @property
    def is_empty(self) -> bool:
        return not self.content.strip()