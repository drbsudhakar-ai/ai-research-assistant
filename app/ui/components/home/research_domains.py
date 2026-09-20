"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/research_domains.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Research domain showcase component.

Responsibilities:
    - Display supported research areas.
    - Communicate application scope.

Non-Responsibilities:
    - Domain classification.
    - AI analysis.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Iterable

import streamlit as st


@dataclass(frozen=True)
class ResearchDomains:
    """
    Represents research areas.
    """

    domains: Iterable[str]


    def render(self) -> None:
        """
        Render research domain list.
        """

        badges = " ".join(
            [
                f"""
                <span class="domain-badge">
                    {domain}
                </span>
                """
                for domain in self.domains
            ]
        )

        render_html(f"""
            <div class="research-domains">

                <h3>
                    🔬 Research Domains
                </h3>

                <div>
                    {badges}
                </div>

            </div>
            """)


def render_research_domains(
    domains: Iterable[str],
) -> None:
    """
    Render research domains.
    """

    ResearchDomains(
        domains=domains,
    ).render()


__all__ = [
    "ResearchDomains",
    "render_research_domains",
]