"""
===============================================================================
Project      : AI Research Assistant
Module       : PDF Utilities
File         : pdf_text_formatter.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Format extracted PDF text for user-friendly display.

Responsibilities:
    - Normalize whitespace.
    - Join wrapped lines.
    - Preserve paragraph breaks.
    - Improve readability.

Business logic and AI logic must not be implemented here.
===============================================================================
"""

from __future__ import annotations

import re

__all__ = [
    "PDFTextFormatter",
]


class PDFTextFormatter:
    """
    Utility class for formatting extracted PDF text.
    """

    @staticmethod
    def format(text: str) -> str:
        """
        Format extracted PDF text for display.

        Parameters
        ----------
        text : str
            Raw extracted PDF text.

        Returns
        -------
        str
            Readable formatted text.
        """

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove trailing spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Join wrapped lines while preserving paragraphs
        text = re.sub(
            r"(?<!\n)\n(?!\n)",
            " ",
            text,
        )

        # Collapse multiple blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()