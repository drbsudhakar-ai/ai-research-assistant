"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/badge.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable badge UI component for Streamlit pages.

Responsibilities:
    - Render compact status/category labels.
    - Provide consistent badge styles.
    - Support different semantic variants.

Non-Responsibilities:
    - Business logic.
    - Status calculation.
    - Data processing.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import streamlit as st

from app.ui.theme.theme_config import UI_THEME, ThemeConfig


class BadgeVariant(str, Enum):
    """
    Supported badge variants.
    """

    DEFAULT = "default"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


@dataclass(frozen=True)
class Badge:
    """
    Represents a small UI badge.

    Attributes:
        text:
            Badge display text.

        variant:
            Badge semantic type.

        icon:
            Optional icon.

        tooltip:
            Optional tooltip text.
    """

    text: str

    variant: BadgeVariant = BadgeVariant.DEFAULT

    icon: Optional[str] = None
    tooltip: Optional[str] = None

    def render(self) -> None:
        """
        Render badge component.
        """

        theme = ThemeConfig()

        variant_colors = {
            BadgeVariant.DEFAULT: theme.colors.SECONDARY,
            BadgeVariant.SUCCESS: theme.colors.SUCCESS,
            BadgeVariant.WARNING: theme.colors.WARNING,
            BadgeVariant.ERROR: theme.colors.ERROR,
            BadgeVariant.INFO: theme.colors.INFO,
        }

        background = variant_colors.get(
            self.variant,
            theme.colors.SECONDARY,
        )

        icon_text = (
            f"{self.icon} "
            if self.icon
            else ""
        )

        tooltip_html = (
            f'title="{self.tooltip}"'
            if self.tooltip
            else ""
        )

        render_html(f"""
            <span class="badge"
                  {tooltip_html}
                  style="
                    background-color:{background};
                  ">
                {icon_text}{self.text}
            </span>
            """)


def render_badge(
    text: str,
    *,
    variant: BadgeVariant = BadgeVariant.DEFAULT,
    icon: Optional[str] = None,
    tooltip: Optional[str] = None,
) -> None:
    """
    Functional helper for badge rendering.

    Example:

        render_badge(
            "Completed",
            variant=BadgeVariant.SUCCESS,
            icon="✅"
        )
    """

    badge = Badge(
        text=text,
        variant=variant,
        icon=icon,
        tooltip=tooltip,
    )

    badge.render()


__all__ = [
    "BadgeVariant",
    "Badge",
    "render_badge",
]