"""
===============================================================================
Project      : AI Research Assistant
Module       : Paper Section Extractor
File         : app/services/paper_section_extractor.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Extracts the logical sections of a research paper using lightweight
    rule-based heading detection.

Responsibilities:
    - Normalize extracted text.
    - Detect common academic section headings.
    - Extract major paper sections.
    - Return an immutable PaperSections model.

Notes:
    - No AI.
    - No LLM.
    - No external NLP libraries.
    - Optimized for IEEE, ACM, Springer, Elsevier and MDPI papers.
===============================================================================
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from app.models.paper_sections import PaperSections

__all__ = [
    "PaperSectionExtractor",
]


# =============================================================================
# Internal Models
# =============================================================================


@dataclass(slots=True, frozen=True)
class _Heading:
    """
    Represents a detected section heading.
    """

    canonical: str
    start: int
    end: int


# =============================================================================
# Extractor
# =============================================================================


class PaperSectionExtractor:
    """
    Lightweight research paper section extractor.
    """

    _NORMALIZE_PATTERN = re.compile(r"[ \t]+")

    _NEWLINES_PATTERN = re.compile(r"\n{3,}")

    _ROMAN = (
        r"(?:[IVXLCDM]+)"
    )

    _NUMBER = (
        r"(?:\d+(?:\.\d+)*)"
    )

    _PREFIX = (
        rf"(?:{_NUMBER}|{_ROMAN})?"
        r"\s*[\.\)]?\s*"
    )

    # =========================================================================
    # Canonical heading aliases
    # =========================================================================

    _SECTION_ALIASES: dict[str, tuple[str, ...]] = {

        "abstract": (
            "abstract",
        ),

        "introduction": (
            "introduction",
            "background",
        ),

        "related_work": (
            "related work",
            "literature review",
            "previous work",
            "prior work",
            "related studies",
        ),

        "methodology": (
            "methodology",
            "methods",
            "materials and methods",
            "research methodology",
            "experimental setup",
            "proposed method",
            "proposed approach",
            "implementation",
        ),

        "results": (
            "results",
            "experiments",
            "experimental results",
            "evaluation",
            "performance evaluation",
            "findings",
        ),

        "discussion": (
            "discussion",
            "analysis",
            "discussion and analysis",
        ),

        "conclusion": (
            "conclusion",
            "conclusions",
            "future work",
            "conclusion and future work",
            "summary",
        ),

        "references": (
            "references",
            "bibliography",
            "works cited",
        ),
    }

    _MAX_SECTION_CHARS = {
        "abstract": 3000,
        "introduction": 5000,
        "related_work": 4000,
        "methodology": 6000,
        "results": 5000,
        "discussion": 4000,
        "conclusion": 3000,
        "references": 1000,
    }

    # =========================================================================

    def __init__(self) -> None:

        self._patterns = (
            self._compile_patterns()
        )

    # =========================================================================
    # Public API
    # =========================================================================

    def extract(
        self,
        *,
        title: str,
        text: str,
    ) -> PaperSections:
        """
        Extract paper sections.

        Parameters
        ----------
        title:
            Paper title.

        text:
            Extracted paper text.

        Returns
        -------
        PaperSections
        """

        if not text.strip():

            return PaperSections(
                title=title,
            )

        cleaned = self._normalize(
            text,
        )

        headings = self._find_headings(
            cleaned,
        )

        if not headings:

            return PaperSections(
                title=title,
            )

        return self._build_sections(
            title=title,
            text=cleaned,
            headings=headings,
        )
        
    # =========================================================================
    # Pattern Compilation
    # =========================================================================

    @classmethod
    def _compile_patterns(
        cls,
    ) -> dict[str, re.Pattern[str]]:
        """
        Compile heading detection patterns.
        """

        patterns: dict[
            str,
            re.Pattern[str],
        ] = {}

        for canonical, aliases in (
            cls._SECTION_ALIASES.items()
        ):

            escaped = (
                re.escape(alias)
                for alias in aliases
            )

            heading_group = "|".join(
                escaped,
            )

            pattern = (
                rf"(?im)^"
                rf"\s*"
                rf"{cls._PREFIX}"
                rf"(?:{heading_group})"
                rf"\s*$"
            )

            patterns[canonical] = re.compile(
                pattern,
            )

        return patterns

    # =========================================================================
    # Text Normalization
    # =========================================================================

    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize extracted paper text.
        """

        text = (
            text
            .replace("\r\n", "\n")
            .replace("\r", "\n")
            .replace("\x0c", "\n")
        )

        lines: list[str] = []

        for line in text.split("\n"):

            cleaned = self._NORMALIZE_PATTERN.sub(
                " ",
                line,
            ).strip()

            lines.append(cleaned)

        text = "\n".join(lines)

        text = self._NEWLINES_PATTERN.sub(
            "\n\n",
            text,
        )

        return text.strip()

    # =========================================================================
    # Heading Detection
    # =========================================================================

    def _find_headings(
        self,
        text: str,
    ) -> list[_Heading]:
        """
        Detect all supported section headings.
        """

        headings: list[_Heading] = []

        for (
            canonical,
            pattern,
        ) in self._patterns.items():

            for match in pattern.finditer(
                text,
            ):

                headings.append(
                    _Heading(
                        canonical=canonical,
                        start=match.start(),
                        end=match.end(),
                    )
                )

        headings.sort(
            key=lambda item: item.start,
        )

        return self._deduplicate(
            headings,
        )

    # =========================================================================
    # Heading Cleanup
    # =========================================================================

    def _deduplicate(
        self,
        headings: Iterable[_Heading],
    ) -> list[_Heading]:
        """
        Remove overlapping headings.
        """

        result: list[_Heading] = []

        previous_end = -1

        for heading in headings:

            if heading.start < previous_end:
                continue

            result.append(
                heading,
            )

            previous_end = heading.end

        return result
    
    # =========================================================================
    # Section Building
    # =========================================================================

    def _build_sections(
        self,
        *,
        title: str,
        text: str,
        headings: list[_Heading],
    ) -> PaperSections:
        """
        Build the PaperSections model from detected headings.
        """

        sections: dict[str, str] = {}

        for index, heading in enumerate(headings):

            if index + 1 < len(headings):
                next_start = headings[index + 1].start
            else:
                next_start = len(text)

            sections[
                heading.canonical
            ] = self._extract_section(
                text=text,
                heading=heading,
                next_start=next_start,
            )

        return PaperSections(
            title=title,
            abstract=sections.get(
                "abstract",
                "",
            ),
            introduction=sections.get(
                "introduction",
                "",
            ),
            related_work=sections.get(
                "related_work",
                "",
            ),
            methodology=sections.get(
                "methodology",
                "",
            ),
            results=sections.get(
                "results",
                "",
            ),
            discussion=sections.get(
                "discussion",
                "",
            ),
            conclusion=sections.get(
                "conclusion",
                "",
            ),
            references=sections.get(
                "references",
                "",
            ),
        )

    # =========================================================================

    def _extract_section(
        self,
        *,
        text: str,
        heading: _Heading,
        next_start: int,
    ) -> str:
        """
        Extract the content belonging to a single section.
        """

        content = text[
            heading.end:next_start
        ]

        return self._clean_section(
            content,
        )

    # =========================================================================

    def _clean_section(
        self,
        content: str,
    ) -> str:
        """
        Clean extracted section text.
        """

        content = content.strip()

        if not content:
            return ""

        lines: list[str] = []

        for line in content.splitlines():

            cleaned = line.strip()

            if not cleaned:
                continue

            lines.append(cleaned)

        content = "\n".join(lines)

        content = self._NEWLINES_PATTERN.sub(
            "\n\n",
            content,
        )

        return content.strip()

    # =========================================================================

    def _get_section(
        self,
        sections: dict[str, str],
        name: str,
    ) -> str:
        """
        Safely return a section.

        Parameters
        ----------
        sections:
            Extracted section dictionary.

        name:
            Canonical section name.

        Returns
        -------
        str
        """

        return sections.get(
            name,
            "",
        )
        
    # =========================================================================
    # Convenience Methods
    # =========================================================================

    @property
    def supported_sections(self) -> tuple[str, ...]:
        """
        Return the canonical section names supported by the extractor.
        """

        return tuple(self._SECTION_ALIASES.keys())

    def has_section(
        self,
        paper_sections: PaperSections,
        section: str,
    ) -> bool:
        """
        Determine whether a section contains content.

        Parameters
        ----------
        paper_sections:
            Extracted paper sections.

        section:
            Canonical section name.

        Returns
        -------
        bool
        """

        if not section:
            return False

        section = section.lower()

        if section not in self.supported_sections:
            return False

        value = getattr(
            paper_sections,
            section,
            "",
        )

        return bool(value.strip())

    def extract_available_sections(
        self,
        paper_sections: PaperSections,
    ) -> dict[str, str]:
        """
        Return only the sections that contain content.

        Parameters
        ----------
        paper_sections:
            Extracted paper sections.

        Returns
        -------
        dict[str, str]
        """

        available: dict[str, str] = {}

        for section in self.supported_sections:

            value = getattr(
                paper_sections,
                section,
                "",
            )

            if value.strip():
                available[section] = value

        return available

    def build_prompt_context(
        self,
        paper_sections: PaperSections,
    ) -> str:
        """
        Build a compact prompt context from extracted sections.

        This helper is intended for PromptBuilder so the LLM
        receives only the meaningful parts of the paper.
        """

        blocks: list[str] = []

        if paper_sections.title:
            blocks.append(
                f"# Title\n\n{paper_sections.title}"
            )

        for section in self.supported_sections:

            value = getattr(
                paper_sections,
                section,
                "",
            ).strip()

            limit = self._MAX_SECTION_CHARS.get(
                section,
                3000,
            )

            value = value[:limit]

            if not value:
                continue

            heading = (
                section
                .replace("_", " ")
                .title()
            )

            blocks.append(
                f"# {heading}\n\n{value}"
            )

        return "\n\n".join(blocks)

    # =========================================================================
    # Representation
    # =========================================================================

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"supported_sections="
            f"{len(self.supported_sections)})"
        )