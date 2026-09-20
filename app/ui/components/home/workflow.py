"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/workflow.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Research analysis workflow visualization component.

Responsibilities:
    - Display AI analysis workflow.
    - Explain processing stages visually.

Non-Responsibilities:
    - Pipeline execution.
    - Progress tracking.
    - Runtime state.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Iterable

import streamlit as st


@dataclass(frozen=True)
class WorkflowStep:
    """
    Represents one workflow stage.
    """

    title: str

    description: str

    icon: str = "➡️"


@dataclass(frozen=True)
class Workflow:
    """
    Represents complete workflow.
    """

    steps: Iterable[WorkflowStep]


    def render(self) -> None:
        """
        Render workflow steps.
        """

        workflow_html = ""

        for step in self.steps:

            workflow_html += f"""
            <div class="workflow-step">

                <h4>
                    {step.icon} {step.title}
                </h4>

                <p>
                    {step.description}
                </p>

            </div>

            <div class="workflow-arrow">
                ↓
            </div>
            """

        render_html(f"""
            <div class="workflow">

                <h3>
                    ⚙️ Research Analysis Workflow
                </h3>

                {workflow_html}

            </div>
            """)


def render_workflow(
    steps: Iterable[WorkflowStep],
) -> None:
    """
    Render workflow visualization.
    """

    Workflow(
        steps=steps,
    ).render()


__all__ = [
    "WorkflowStep",
    "Workflow",
    "render_workflow",
]