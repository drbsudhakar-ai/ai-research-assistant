"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/analyze/progress_panel.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Analysis pipeline progress visualization.

Responsibilities:
    - Display progress percentage.
    - Show current pipeline stage.
    - Present execution status.

Non-Responsibilities:
    - Progress calculation.
    - Pipeline execution.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class ProgressPanel:
    """
    Pipeline progress display.
    """

    percentage: int

    stage: str

    message: str = ""


    def render(self):
        """
        Render progress panel.
        """

        st.progress(
            self.percentage / 100
        )

        st.caption(
            f"{self.stage} - {self.percentage}%"
        )

        if self.message:
            st.info(
                self.message
            )


def render_progress_panel(
    percentage: int,
    stage: str,
    message: str = "",
):
    """
    Render progress panel.
    """

    ProgressPanel(
        percentage=percentage,
        stage=stage,
        message=message,
    ).render()


__all__ = [
    "ProgressPanel",
    "render_progress_panel",
]