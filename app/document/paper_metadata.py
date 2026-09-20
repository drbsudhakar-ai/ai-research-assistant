"""
===============================================================================
Project      : AI Research Assistant
Module       : Document Model
File         : paper_metadata.py
Version      : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PaperMetadata:
    """
    Metadata extracted from a research paper.

    This model intentionally contains only descriptive information
    about the paper and does not contain document content.
    """

    title: str = ""

    authors: list[str] = field(default_factory=list)

    affiliations: list[str] = field(default_factory=list)

    keywords: list[str] = field(default_factory=list)

    doi: str | None = None

    journal: str | None = None

    conference: str | None = None

    publication_year: int | None = None

    language: str = "unknown"

    page_count: int = 0

    character_count: int = 0

    word_count: int = 0