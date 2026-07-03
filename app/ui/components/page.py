"""
===============================================================================
Project      : AI Research Assistant
File         : page.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Reusable page layout components.

Responsibilities:
    - Render standardized page headers.
    - Render section headers.
    - Render page dividers.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import streamlit as st

__all__ = [
    "render_page_header",
    "render_section_header",
    "render_divider",
]


# =============================================================================
# Public API
# =============================================================================

def render_page_header(
    title: str,
    description: str | None = None,
) -> None:
    """
    Render a standardized page header.

    Parameters
    ----------
    title : str
        Page title.

    description : str | None
        Optional page description.
    """

    st.title(title)

    if description:
        st.caption(description)

    st.divider()


def render_section_header(title: str) -> None:
    """
    Render a standardized section header.

    Parameters
    ----------
    title : str
        Section title.
    """

    st.subheader(title)


def render_divider() -> None:
    """Render a horizontal divider."""

    st.divider()