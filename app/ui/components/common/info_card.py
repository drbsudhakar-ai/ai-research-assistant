"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/info_card.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable information card UI component for Streamlit pages.

Responsibilities:
    - Display informational content in a consistent card layout.
    - Support titles, descriptions, icons, and optional actions.
    - Provide reusable UI building blocks across application pages.

Non-Responsibilities:
    - Data loading.
    - Business logic.
    - Pipeline execution.
    - Application state management.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from app.ui.theme.theme_config import ThemeConfig


@dataclass(frozen=True)
class InfoCard:
    """
    Represents a reusable information card.

    Attributes:
        title:
            Card heading text.

        content:
            Main informational message.

        icon:
            Optional emoji/icon displayed before title.

        footer:
            Optional footer/helper text.

        accent:
            Optional accent color override.
    """

    title: str
    content: str

    icon: Optional[str] = None
    footer: Optional[str] = None
    accent: Optional[str] = None

    def render(self) -> None:
        """
        Render information card using Streamlit markdown.
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

        footer_html = (
            f"""
            <div class="info-card-footer">
                {self.footer}
            </div>
            """
            if self.footer
            else ""
        )

        render_html(f"""
            <div class="info-card"
                 style="
                    border-left: 5px solid {accent_color};
                 ">

                <div class="info-card-title">
                    {icon_text}{self.title}
                </div>

                <div class="info-card-content">
                    {self.content}
                </div>

                {footer_html}

            </div>
            """)


def render_info_card(
    title: str,
    content: str,
    *,
    icon: Optional[str] = None,
    footer: Optional[str] = None,
    accent: Optional[str] = None,
) -> None:
    """
    Functional helper for rendering information cards.

    Example:
        render_info_card(
            title="Research Assistant",
            content="Analyze research papers using AI.",
            icon="🤖"
        )
    """

    card = InfoCard(
        title=title,
        content=content,
        icon=icon,
        footer=footer,
        accent=accent,
    )

    card.render()


__all__ = [
    "InfoCard",
    "render_info_card",
]