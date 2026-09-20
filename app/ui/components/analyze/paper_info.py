"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/analyze/paper_info.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Paper metadata display component.

Responsibilities:
    - Display extracted paper information.
    - Show document statistics.

Non-Responsibilities:
    - PDF extraction.
    - Metadata generation.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class PaperInfo:
    """
    Research paper information.
    """

    title: str

    pages: int

    characters: int

    source: str = "PDF"


    def render(self):
        """
        Render paper information.
        """

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Title",
                self.title,
            )

        with col2:
            st.metric(
                "Pages",
                self.pages,
            )

        with col3:
            st.metric(
                "Characters",
                self.characters,
            )


def render_paper_info(
    *,
    title: str,
    pages: int,
    characters: int,
):
    """
    Render paper information.
    """

    PaperInfo(
        title=title,
        pages=pages,
        characters=characters,
    ).render()


__all__ = [
    "PaperInfo",
    "render_paper_info",
]