"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme Framework
File         : theme_loader.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Loads and injects all global CSS resources required by the UI.

Responsibilities:
    - Load CSS files.
    - Inject CSS into Streamlit.
    - Prevent duplicate injections.
    - Cache CSS content.

Non-Responsibilities:
    - Theme selection.
    - Component rendering.
    - Page configuration.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from pathlib import Path

import streamlit as st


class ThemeLoader:
    """
    Loads and injects global CSS resources.
    """

    _loaded: bool = False

    _CSS_FILES = (
        "theme.css",
        "cards.css",
    )

    @classmethod
    def load(cls) -> None:
        """
        Load all CSS files once.
        """

        if cls._loaded:
            return

        css_root = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "assets"
            / "css"
        )

        css = []

        for file_name in cls._CSS_FILES:

            css_file = css_root / file_name

            if not css_file.exists():
                raise FileNotFoundError(
                    f"CSS file not found: {css_file}"
                )

            css.append(
                css_file.read_text(
                    encoding="utf-8"
                )
            )

        render_html(f"<style>{''.join(css)}</style>")

        cls._loaded = True