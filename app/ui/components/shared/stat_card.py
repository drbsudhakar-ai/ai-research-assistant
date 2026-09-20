"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/shared/stat_card.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable statistical metric card component.

    Provides:
        - Dashboard metrics
        - Trend indicators
        - Icons
        - Theme-aware rendering

Dependencies:
        - Streamlit
        - Theme System

===============================================================================
"""


from __future__ import annotations

from app.ui.html_renderer import render_html

from dataclasses import dataclass
from typing import Optional, Literal


import streamlit as st



from app.ui.theme import (
    ThemeManager,
)



# =============================================================================
# Data Model
# =============================================================================


TrendType = Literal[
    "positive",
    "negative",
    "neutral",
]



@dataclass(
    frozen=True,
)
class StatValue:
    """
    Represents metric information.

    Attributes:
        label:
            Metric name.

        value:
            Main displayed value.

        description:
            Supporting information.

        trend:
            Trend direction.

        icon:
            Optional emoji/icon.
    """

    label: str

    value: str

    description: Optional[str] = None

    trend: TrendType = "neutral"

    icon: Optional[str] = None



# =============================================================================
# Stat Card Component
# =============================================================================


class StatCard:
    """
    Dashboard metric card renderer.

    Example:

        StatCard.render(
            label="Papers Analyzed",
            value="125",
            description="This month",
            trend="positive",
            icon="📄",
        )

    """



    # -------------------------------------------------------------------------
    # Render Single Card
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        *,
        label: str,
        value: str,
        description: Optional[str] = None,
        trend: TrendType = "neutral",
        icon: Optional[str] = None,
    ) -> None:
        """
        Render metric card.

        Args:
            label:
                Metric title.

            value:
                Main metric value.

            description:
                Supporting text.

            trend:
                positive / negative / neutral.

            icon:
                Optional visual indicator.
        """

        ThemeManager.initialize()


        icon_html = ""


        if icon:

            icon_html = f"""
            <span class="metric-icon">
                {icon}
            </span>
            """



        trend_class = {

            "positive":
                "metric-positive",

            "negative":
                "metric-negative",

            "neutral":
                "",

        }.get(
            trend,
            "",
        )



        description_html = ""


        if description:

            description_html = f"""
            <div class="metric-label">
                {description}
            </div>
            """



        render_html(f"""
            <div class="metric-card">

                {icon_html}

                <div class="metric-value">
                    {value}
                </div>


                <div class="metric-label">
                    {label}
                </div>


                {description_html}


                <div class="
                    metric-change
                    {trend_class}
                ">
                    {StatCard._trend_symbol(trend)}
                </div>


            </div>
            """)



    # -------------------------------------------------------------------------
    # Render Multiple Cards
    # -------------------------------------------------------------------------

    @staticmethod
    def render_group(
        cards: list[StatValue],
        columns: int = 4,
    ) -> None:
        """
        Render multiple metric cards.

        Args:
            cards:
                List of StatValue objects.

            columns:
                Number of columns.
        """

        ThemeManager.initialize()


        layout = st.columns(
            columns
        )


        for index, card in enumerate(cards):

            with layout[index % columns]:

                StatCard.render(

                    label=card.label,

                    value=card.value,

                    description=card.description,

                    trend=card.trend,

                    icon=card.icon,

                )



    # -------------------------------------------------------------------------
    # Trend Indicator
    # -------------------------------------------------------------------------

    @staticmethod
    def _trend_symbol(
        trend: TrendType,
    ) -> str:
        """
        Return trend indicator.

        Args:
            trend:
                Trend state.

        Returns:
            str:
                Symbol.
        """

        symbols = {

            "positive":
                "▲ Improving",

            "negative":
                "▼ Decreasing",

            "neutral":
                "● Stable",

        }


        return symbols.get(
            trend,
            "",
        )



    # -------------------------------------------------------------------------
    # Common Research Metrics Preset
    # -------------------------------------------------------------------------

    @staticmethod
    def research_metrics(
        *,
        papers: int,
        pages: int,
        models: int,
        history: int,
    ) -> None:
        """
        Render standard research dashboard metrics.

        Args:
            papers:
                Total analyzed papers.

            pages:
                Total pages processed.

            models:
                Available AI models.

            history:
                Stored analyses.
        """

        StatCard.render_group(

            [

                StatValue(
                    label="Papers Analyzed",
                    value=str(papers),
                    description="Total processed",
                    trend="positive",
                    icon="📄",
                ),


                StatValue(
                    label="Pages Processed",
                    value=str(pages),
                    description="Research content",
                    trend="positive",
                    icon="📚",
                ),


                StatValue(
                    label="AI Models",
                    value=str(models),
                    description="Available providers",
                    trend="neutral",
                    icon="🤖",
                ),


                StatValue(
                    label="History Records",
                    value=str(history),
                    description="Stored analyses",
                    trend="positive",
                    icon="🗂️",
                ),

            ]

        )