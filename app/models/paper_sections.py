"""
===============================================================================
Project      : AI Research Assistant
Module       : Models
File         : paper_sections.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Immutable model representing the major logical sections extracted
    from a research paper.

Responsibilities:
    - Store extracted paper sections.
    - Provide a stable contract between the PaperSectionExtractor and
      PromptBuilder.
    - Keep section extraction independent from AI analysis.

Notes:
    - Immutable.
    - No business logic.
    - No Streamlit dependency.
    - No database dependency.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "PaperSections",
]


@dataclass(slots=True, frozen=True)
class PaperSections:
    """
    Represents the major sections of a research paper.

    All fields default to an empty string so downstream components
    never fail when a section is missing.
    """

    title: str = ""

    abstract: str = ""

    introduction: str = ""

    related_work: str = ""

    methodology: str = ""

    results: str = ""

    discussion: str = ""

    conclusion: str = ""

    references: str = ""

    # =========================================================================
    # Convenience Properties
    # =========================================================================

    @property
    def has_abstract(self) -> bool:
        """Return True if the abstract is available."""

        return bool(self.abstract.strip())

    @property
    def has_introduction(self) -> bool:
        """Return True if the introduction is available."""

        return bool(self.introduction.strip())

    @property
    def has_related_work(self) -> bool:
        """Return True if related work is available."""

        return bool(self.related_work.strip())

    @property
    def has_methodology(self) -> bool:
        """Return True if methodology is available."""

        return bool(self.methodology.strip())

    @property
    def has_results(self) -> bool:
        """Return True if results are available."""

        return bool(self.results.strip())

    @property
    def has_discussion(self) -> bool:
        """Return True if discussion is available."""

        return bool(self.discussion.strip())

    @property
    def has_conclusion(self) -> bool:
        """Return True if conclusion is available."""

        return bool(self.conclusion.strip())

    @property
    def has_references(self) -> bool:
        """Return True if references are available."""

        return bool(self.references.strip())

    @property
    def available_sections(self) -> list[str]:
        """
        Return a list containing the names of available sections.
        """

        sections: list[str] = []

        if self.has_abstract:
            sections.append("Abstract")

        if self.has_introduction:
            sections.append("Introduction")

        if self.has_related_work:
            sections.append("Related Work")

        if self.has_methodology:
            sections.append("Methodology")

        if self.has_results:
            sections.append("Results")

        if self.has_discussion:
            sections.append("Discussion")

        if self.has_conclusion:
            sections.append("Conclusion")

        if self.has_references:
            sections.append("References")

        return sections

    @property
    def section_count(self) -> int:
        """
        Return the number of extracted sections.
        """

        return len(self.available_sections)

    @property
    def is_empty(self) -> bool:
        """
        Return True when no sections were extracted.
        """

        return self.section_count == 0

    def __len__(self) -> int:
        """Return the number of extracted sections."""

        return self.section_count

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"sections={self.section_count}, "
            f"available={self.available_sections})"
        )