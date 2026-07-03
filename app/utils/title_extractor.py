"""
===============================================================================
Project      : AI Research Assistant
Module       : PDF Utilities
File         : title_extractor.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
    Extract research paper titles from PDF documents.

Responsibilities:
    - Extract metadata title candidates.
    - Extract layout title candidates.
    - Score title candidates.
    - Select the best title candidate.

Notes:
    - This module contains no Streamlit code.
    - This module contains no AI logic.
===============================================================================
"""

from __future__ import annotations

import os
import re

from dataclasses import dataclass

import fitz


__all__ = [
    "TitleCandidate",
    "TitleResult",
    "TitleExtractor",
]


# =============================================================================
# Data Models
# =============================================================================


@dataclass(slots=True, frozen=True)
class TitleCandidate:
    """
    Intermediate title candidate.
    """

    title: str
    confidence: float
    source: str

    font_size: float
    top: float
    left: float
    width: float

    line_count: int
    word_count: int


@dataclass(slots=True, frozen=True)
class TitleResult:
    """
    Final title extraction result.
    """

    title: str
    confidence: float
    source: str

# =============================================================================
# Title Extractor
# =============================================================================

class TitleExtractor:
    """
    Extract titles from research papers.
    """

    INVALID_METADATA = (
        "microsoft",
        "adobe",
        "acrobat",
        "word",
        "document",
        "untitled",
        "draft",
        "copy",
        "sample",
        "final",
    )

    HEADER_WORDS = (
        "ieee",
        "transactions",
        "springer",
        "elsevier",
        "wiley",
        "copyright",
        "digital object identifier",
        "doi",
        "accepted",
        "publication",
    )

    AUTHOR_WORDS = (
        "university",
        "department",
        "school",
        "laboratory",
        "laboratories",
        "institute",
        "@",
        "member, ieee",
    )
    
    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    
    @classmethod
    def extract(
        cls,
        document: fitz.Document,
    ) -> TitleResult:
        """
        Extract the best title from a PDF.
        """

        candidates: list[TitleCandidate] = []

        metadata = cls._extract_metadata_candidate(
            document,
        )

        if metadata is not None:
            candidates.append(metadata)

        candidates.extend(
            cls._extract_layout_candidates(
                document,
            )
        )

        if not candidates:
            return TitleResult(
                title="Unknown Title",
                confidence=0.0,
                source="none",
            )

        best = max(
            candidates,
            key=lambda item: item.confidence,
        )

        return TitleResult(
            title=best.title,
            confidence=best.confidence,
            source=best.source,
        )


    # -------------------------------------------------------------------------
    # Metadata Extraction
    # -------------------------------------------------------------------------

    @classmethod
    def _extract_metadata_candidate(
        cls,
        document: fitz.Document,
    ) -> TitleCandidate | None:

        metadata = document.metadata or {}

        title = metadata.get(
            "title",
            "",
        ).strip()

        if not title:
            return None

        if cls._looks_like_filename(title):
            return None

        lower = title.lower()

        if any(
            word in lower
            for word in cls.INVALID_METADATA
        ):
            return None

        if len(title.split()) < 4:
            return None

        
        return TitleCandidate(
            title=cls._clean(title),
            confidence=0.80,
            source="metadata",
            font_size=0.0,
            top=0.0,
            left=0.0,
            width=0.0,
            line_count=1,
            word_count=len(title.split()),
        )

    @staticmethod
    def _looks_like_filename(
        text: str,
    ) -> bool:

        lower = os.path.basename(
            text,
        ).lower()

        extensions = (
            ".pdf",
            ".doc",
            ".docx",
            ".ppt",
            ".pptx",
            ".xls",
            ".xlsx",
        )

        if lower.endswith(
            extensions,
        ):
            return True

        return False



    @staticmethod
    def _clean(
        text: str,
    ) -> str:

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()



    # -------------------------------------------------------------------------
    # Layout Extraction
    # -------------------------------------------------------------------------

    @classmethod
    def _extract_layout_candidates(
        cls,
        document: fitz.Document,
    ) -> list[TitleCandidate]:
        """
        Extract title candidates from the first page layout.
        """

        page = document[0]

        page_dict = page.get_text("dict")

        page_width = page.rect.width
        page_height = page.rect.height

        candidates: list[TitleCandidate] = []

        for block in page_dict.get("blocks", []):

            if "lines" not in block:
                continue

            text_parts: list[str] = []

            max_font = 0.0
            min_top = float("inf")
            min_left = float("inf")
            max_right = 0.0

            line_count = 0

            for line in block["lines"]:

                line_text: list[str] = []

                has_text = False

                for span in line.get("spans", []):

                    text = span["text"].strip()

                    if not text:
                        continue

                    has_text = True

                    line_text.append(text)

                    max_font = max(
                        max_font,
                        span["size"],
                    )

                    x0, y0, x1, y1 = span["bbox"]

                    min_top = min(min_top, y0)
                    min_left = min(min_left, x0)
                    max_right = max(max_right, x1)

                if has_text:

                    line_count += 1

                    text_parts.append(
                        " ".join(line_text)
                    )

            if not text_parts:
                continue

            block_text = cls._clean(
                " ".join(text_parts)
            )

            if len(block_text) < 10:
                continue

            word_count = len(
                block_text.split()
            )

            width = max_right - min_left

            score = cls._score_candidate_values(
                text=block_text,
                font_size=max_font,
                top=min_top,
                width=width,
                line_count=line_count,
                word_count=word_count,
                page_width=page_width,
                page_height=page_height,
            )

            candidates.append(
                TitleCandidate(
                    title=block_text,
                    confidence=score,
                    source="layout",
                    font_size=max_font,
                    top=min_top,
                    left=min_left,
                    width=width,
                    line_count=line_count,
                    word_count=word_count,
                )
            )

        return candidates
        
    # -------------------------------------------------------------------------
    # Candidate Scoring
    # -------------------------------------------------------------------------
        
    @staticmethod
    def _score_font(
        font_size: float,
    ) -> float:

        if font_size >= 20:
            return 0.35

        if font_size >= 18:
            return 0.30

        if font_size >= 16:
            return 0.25

        if font_size >= 14:
            return 0.15

        return 0.05

    @staticmethod
    def _score_position(
        top: float,
        page_height: float,
    ) -> float:

        ratio = top / page_height

        if ratio <= 0.20:
            return 0.20

        if ratio <= 0.30:
            return 0.15

        if ratio <= 0.40:
            return 0.10

        return 0.0

    @staticmethod
    def _score_word_count(
        words: int,
    ) -> float:

        if 5 <= words <= 20:
            return 0.15

        if 4 <= words <= 25:
            return 0.10

        return 0.0

    @staticmethod
    def _score_line_count(
        lines: int,
    ) -> float:

        if lines == 1:
            return 0.10

        if lines == 2:
            return 0.08

        if lines == 3:
            return 0.05

        return 0.0

    @staticmethod
    def _score_width(
        width: float,
        page_width: float,
    ) -> float:

        ratio = width / page_width

        if ratio >= 0.60:
            return 0.10

        if ratio >= 0.40:
            return 0.05

        return 0.0

    @classmethod
    def _score_text(
        cls,
        text: str,
    ) -> float:

        lower = text.lower()

        score = 0.0

        if any(
            word in lower
            for word in cls.HEADER_WORDS
        ):
            score -= 0.60

        if any(
            word in lower
            for word in cls.AUTHOR_WORDS
        ):
            score -= 0.50

        if "abstract" in lower:
            score -= 0.40

        if "keywords" in lower:
            score -= 0.40

        if "introduction" in lower:
            score -= 0.30

        if "@" in lower:
            score -= 0.50

        return score
    
    @classmethod
    def _score_candidate_values(
        cls,
        *,
        text: str,
        font_size: float,
        top: float,
        width: float,
        line_count: int,
        word_count: int,
        page_width: float,
        page_height: float,
    ) -> float:
        """
        Calculate the confidence score for a potential title.
        """

        score = 0.0

        score += cls._score_font(font_size)

        score += cls._score_position(
            top,
            page_height,
        )

        score += cls._score_word_count(
            word_count,
        )

        score += cls._score_line_count(
            line_count,
        )

        score += cls._score_width(
            width,
            page_width,
        )

        score += cls._score_text(
            text,
        )

        return max(
            0.0,
            min(score, 1.0),
        )