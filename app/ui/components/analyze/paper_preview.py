"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/analyze/paper_preview.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Extracted paper text preview component.

Responsibilities:
    - Display extracted text preview.
    - Control preview visibility.

Non-Responsibilities:
    - Text extraction.
    - PDF processing.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class PaperPreview:
    """
    Text preview component.
    """

    text: str

    max_length: int = 3000


    def render(self):
        """
        Render extracted text.
        """

        preview = self.text[
            : self.max_length
        ]

        with st.expander(
            "📄 Paper Preview",
            expanded=False,
        ):
            st.text(preview)


def render_paper_preview(
    text: str,
):
    """
    Render paper preview.
    """

    PaperPreview(
        text=text,
    ).render()


__all__ = [
    "PaperPreview",
    "render_paper_preview",
]