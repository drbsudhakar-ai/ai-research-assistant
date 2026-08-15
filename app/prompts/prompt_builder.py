"""
===============================================================================
Project      : AI Research Assistant
Module       : Prompt Builder
File         : prompt_builder.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
    Builds optimized prompts for research paper analysis.

Responsibilities:
    - Extract major paper sections.
    - Build a compact, high-quality prompt.
    - Hide prompt construction details from the analyzer.
    - Reduce LLM input size while preserving context.

Notes:
    - Version 2.0 introduces lightweight section extraction.
    - Fully compatible with future multi-agent architecture.
===============================================================================
"""

from __future__ import annotations

from app.models.prepared_paper import PreparedPaper
from app.prompts.research.paper_analysis_prompt import (
    build_paper_analysis_prompt,
)
from app.services.paper_section_extractor import (
    PaperSectionExtractor,
)
import logging

_LOGGER = logging.getLogger(__name__)


__all__ = [
    "PromptBuilder",
]


class PromptBuilder:
    """
    Builds optimized prompts for research paper analysis.
    """

    def __init__(
        self,
        section_extractor: (
            PaperSectionExtractor | None
        ) = None,
    ) -> None:
        """
        Initialize prompt builder.

        Parameters
        ----------
        section_extractor:
            Lightweight paper section extractor.
        """

        self._extractor = (
            section_extractor
            or PaperSectionExtractor()
        )

    # =========================================================================
    # Public API
    # =========================================================================

    def build(
        self,
        paper: PreparedPaper,
    ) -> str:
        """
        Build the optimized user prompt.
        """

        if paper is None:
            raise ValueError(
                "paper cannot be None."
            )

        if not paper.text.strip():
            raise ValueError(
                "Paper text is empty."
            )

        sections = self._extractor.extract(
            title=paper.title,
            text=paper.text,
        )

        # ---------------------------------------------------------
        # Log extracted section statistics
        # ---------------------------------------------------------
        available_sections = (
            self._extractor.extract_available_sections(
                sections,
            )
        )

        for name, content in available_sections.items():

            _LOGGER.info(
                "Section '%s': %d characters",
                name,
                len(content),
            )

        context = (
            self._extractor.build_prompt_context(
                sections,
            )
        )

        prompt = build_paper_analysis_prompt(
            context,
        )

        _LOGGER.info(
            "Prompt statistics | Context: %d chars | Prompt: %d chars",
            len(context),
            len(prompt),
        )

        return prompt
