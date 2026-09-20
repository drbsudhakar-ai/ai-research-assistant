"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/section_header.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable section header UI component for Streamlit pages.

Responsibilities:
    - Render consistent section headings across the application.
    - Support titles, subtitles, icons, and visual hierarchy.
    - Maintain professional UI consistency.

Non-Responsibilities:
    - Page navigation.
    - Business logic.
    - Data processing.
    - Pipeline execution.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from app.ui.theme.theme_config import ThemeConfig


@dataclass(frozen=True)
class SectionHeader:
    """
    Represents a reusable section header.

    Attributes:
        title:
            Main section title.

        subtitle:
            Optional supporting description.

        icon:
            Optional emoji/icon displayed before title.

        level:
            Header hierarchy level (1-6).

        accent:
            Optional accent color override.
    """

    title: str

    subtitle: Optional[str] = None
    icon: Optional[str] = None

    level: int = 2

    accent: Optional[str] = None

    def render(self) -> None:
        """
        Render section header.
        """

        theme = ThemeConfig()

        accent_color = (
            self.accent
            if self.accent
            else theme.colors.primary
        )

        icon_text = (
            f"{self.icon} "
            if self.icon
            else ""
        )

        heading_level = min(
            max(self.level, 1),
            6,
        )

        subtitle_html = (
            f"""
            <div class="section-subtitle">
                {self.subtitle}
            </div>
            """
            if self.subtitle
            else ""
        )

        render_html(f"""
            <div class="section-header"
                 style="
                    border-left: 5px solid {accent_color};
                 ">

                <h{heading_level}>
                    {icon_text}{self.title}
                </h{heading_level}>

                {subtitle_html}

            </div>
            """)


def render_section_header(
    title: str,
    *,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    level: int = 2,
    accent: Optional[str] = None,
) -> None:
    """
    Functional helper for rendering section headers.

    Examples:

        render_section_header(
            "Upload Research Paper",
            icon="📄",
            subtitle="Select a PDF file for AI-powered analysis"
        )

        render_section_header(
            "Analysis Results",
            icon="🤖",
            level=2
        )
    """

    header = SectionHeader(
        title=title,
        subtitle=subtitle,
        icon=icon,
        level=level,
        accent=accent,
    )

    header.render()


__all__ = [
    "SectionHeader",
    "render_section_header",
]