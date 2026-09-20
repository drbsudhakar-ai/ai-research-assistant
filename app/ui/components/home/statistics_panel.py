"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/statistics_panel.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Statistics panel component for Home dashboard.

Responsibilities:
    - Display application metrics.
    - Present high-level statistics.

Non-Responsibilities:
    - Database queries.
    - Metric calculation.
    - Business logic.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import streamlit as st

from app.ui.components.common.metric_card import (
    render_metric_card,
)


@dataclass(frozen=True)
class StatisticItem:
    """
    Single statistic entry.
    """

    title: str
    value: str

    icon: str = "📊"


@dataclass(frozen=True)
class StatisticsPanel:
    """
    Home statistics section.
    """

    statistics: Iterable[StatisticItem]


    def render(self) -> None:
        """
        Render statistics cards.
        """

        columns = st.columns(
            len(list(self.statistics))
        )

        for column, item in zip(
            columns,
            self.statistics,
        ):
            with column:
                render_metric_card(
                    title=item.title,
                    value=item.value,
                    icon=item.icon,
                )


def render_statistics_panel(
    statistics: Iterable[StatisticItem],
) -> None:
    """
    Render statistics panel.
    """

    StatisticsPanel(
        statistics=statistics,
    ).render()


__all__ = [
    "StatisticItem",
    "StatisticsPanel",
    "render_statistics_panel",
]