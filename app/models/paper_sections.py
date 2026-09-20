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

from dataclasses import asdict, dataclass
from typing import Any, Final

from app.models.exceptions import DomainValidationError

__all__ = [
    "BODY_SECTION_FIELDS",
    "PaperSections",
]

BODY_SECTION_FIELDS: Final[tuple[str, ...]] = (
    "abstract",
    "introduction",
    "related_work",
    "methodology",
    "results",
    "discussion",
    "conclusion",
    "references",
)

_BODY_DISPLAY_NAMES: Final[dict[str, str]] = {
    "abstract": "Abstract",
    "introduction": "Introduction",
    "related_work": "Related Work",
    "methodology": "Methodology",
    "results": "Results",
    "discussion": "Discussion",
    "conclusion": "Conclusion",
    "references": "References",
}


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

    def __post_init__(self) -> None:
        for field_name in ("title", *BODY_SECTION_FIELDS):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise DomainValidationError(
                    f"{field_name} must be a string.",
                    field=field_name,
                )

    @property
    def has_title(self) -> bool:
        return bool(self.title.strip())

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
        """Return display names of non-empty body sections.

        ``title`` is document identity, not a counted body section.
        Prefer ``section_count`` over ``len(...)``.
        """

        return [
            _BODY_DISPLAY_NAMES[name]
            for name in BODY_SECTION_FIELDS
            if str(getattr(self, name)).strip()
        ]

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PaperSections:
        allowed = {"title", *BODY_SECTION_FIELDS}
        unknown = set(data) - allowed
        if unknown:
            raise DomainValidationError(
                f"Unknown PaperSections fields: {sorted(unknown)}.",
            )
        return cls(**{key: data.get(key, "") for key in allowed if key in data})

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
