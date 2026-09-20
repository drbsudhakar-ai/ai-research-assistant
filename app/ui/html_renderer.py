"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/html_renderer.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Safe HTML rendering helpers for Streamlit.

    Streamlit markdown treats indented HTML as code blocks. These helpers
    normalize content and render it with ``st.html`` instead.
===============================================================================
"""

from __future__ import annotations

from textwrap import dedent

import streamlit as st

__all__ = [
    "render_html",
    "render_sidebar_html",
    "render_css",
]


def render_html(html: str) -> None:
    """
    Render raw HTML in Streamlit.

    Args:
        html:
            HTML fragment to render.
    """

    st.html(
        dedent(html).strip()
    )


def render_sidebar_html(html: str) -> None:
    """
    Render raw HTML in the Streamlit sidebar.

    Args:
        html:
            HTML fragment to render.
    """

    st.sidebar.html(
        dedent(html).strip()
    )


def render_css(css: str) -> None:
    """
    Inject CSS into the active Streamlit page.

    Args:
        css:
            CSS stylesheet content without ``<style>`` tags.
    """

    st.html(
        f"<style>{dedent(css).strip()}</style>"
    )
