"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/metric_card.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable metric card UI component for Streamlit pages.

Responsibilities:
    - Render professional KPI/statistic cards.
    - Provide consistent styling across the application.
    - Support optional icons, labels, values, and descriptions.

Non-Responsibilities:
    - Data retrieval.
    - Business logic.
    - State management.
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
class MetricCard:
    """
    Represents a reusable metric card component.

    Attributes:
        title:
            Metric title displayed above the value.

        value:
            Main metric value.

        icon:
            Optional emoji/icon displayed with title.

        description:
            Supporting text displayed below value.

        accent:
            Optional accent color override.
    """

    title: str
    value: str | int | float

    icon: Optional[str] = None
    description: Optional[str] = None
    accent: Optional[str] = None

    def render(self) -> None:
        """
        Render metric card in Streamlit UI.
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

        description_html = (
            f"""
            <div class="metric-description">
                {self.description}
            </div>
            """
            if self.description
            else ""
        )

        render_html(f"""
            <div class="metric-card"
                 style="
                    border-left: 5px solid {accent_color};
                 ">

                <div class="metric-title">
                    {icon_text}{self.title}
                </div>

                <div class="metric-value">
                    {self.value}
                </div>

                {description_html}

            </div>
            """)


def render_metric_card(
    title: str,
    value: str | int | float,
    *,
    icon: Optional[str] = None,
    description: Optional[str] = None,
    accent: Optional[str] = None,
) -> None:
    """
    Functional helper for quick metric card rendering.

    Example:
        render_metric_card(
            title="Papers Analyzed",
            value=25,
            icon="📄",
            description="Total research papers processed"
        )
    """

    card = MetricCard(
        title=title,
        value=value,
        icon=icon,
        description=description,
        accent=accent,
    )

    card.render()


__all__ = [
    "MetricCard",
    "render_metric_card",
]