"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/empty_state.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable empty state UI component for Streamlit pages.

Responsibilities:
    - Display meaningful messages when no data is available.
    - Provide guidance and optional call-to-action text.
    - Maintain consistent empty-state UX.

Non-Responsibilities:
    - Data retrieval.
    - Navigation handling.
    - Business logic.
    - State management.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from app.ui.theme.theme_config import ThemeConfig


@dataclass(frozen=True)
class EmptyState:
    """
    Represents an empty state display.

    Attributes:
        title:
            Empty state heading.

        message:
            Explanation shown to user.

        icon:
            Optional icon.

        action_text:
            Optional suggested action.

        accent:
            Optional accent color override.
    """

    title: str
    message: str

    icon: Optional[str] = None
    action_text: Optional[str] = None
    accent: Optional[str] = None

    def render(self) -> None:
        """
        Render empty state component.
        """

        theme = ThemeConfig()

        accent_color = (
            self.accent
            if self.accent
            else theme.colors.primary
        )

        icon_text = (
            self.icon
            if self.icon
            else "ℹ️"
        )

        action_html = (
            f"""
            <div class="empty-state-action">
                {self.action_text}
            </div>
            """
            if self.action_text
            else ""
        )

        render_html(f"""
            <div class="empty-state"
                 style="
                    border-left: 5px solid {accent_color};
                 ">

                <div class="empty-state-icon">
                    {icon_text}
                </div>

                <div class="empty-state-title">
                    {self.title}
                </div>

                <div class="empty-state-message">
                    {self.message}
                </div>

                {action_html}

            </div>
            """)


def render_empty_state(
    title: str,
    message: str,
    *,
    icon: Optional[str] = None,
    action_text: Optional[str] = None,
    accent: Optional[str] = None,
) -> None:
    """
    Functional helper for rendering empty states.

    Example:

        render_empty_state(
            title="No Analysis History",
            message="Upload and analyze your first research paper.",
            icon="📚"
        )
    """

    state = EmptyState(
        title=title,
        message=message,
        icon=icon,
        action_text=action_text,
        accent=accent,
    )

    state.render()


__all__ = [
    "EmptyState",
    "render_empty_state",
]