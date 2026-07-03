"""
===============================================================================
Project      : AI Research Assistant
File         : dashboard.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Dashboard page.

Responsibilities:
    - Display application overview.
    - Display quick actions.
    - Display application statistics.
    - Display getting started guide.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from app.ui.components.page import (
    render_divider,
    render_page_header,
    render_section_header,
)

__all__ = [
    "show_dashboard_page",
]


# =============================================================================
# Private Components
# =============================================================================

def _render_header() -> None:
    """Render the dashboard header."""

    render_page_header(
        title="📊 Dashboard",
        description="Welcome to AI Research Assistant.",
    )


def _render_welcome() -> None:
    """Render the welcome message."""

    st.write(
        """
        Welcome to **AI Research Assistant**.

        Analyze research papers, generate AI-powered insights,
        and organize your research workflow from one place.
        """
    )


def _render_quick_actions() -> None:
    """Render quick actions."""

    render_section_header("🚀 Quick Actions")

    st.info(
        """
        • 📄 Analyze a research paper

        • 🕒 View previous analyses

        • ⚙️ Configure AI models
        """
    )


def _render_statistics() -> None:
    """Render application statistics."""

    render_section_header("📈 Application Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Papers Analyzed", 0)

    with col2:
        st.metric("Saved Reports", 0)

    with col3:
        st.metric("Active Model", "Not Configured")


def _render_getting_started() -> None:
    """Render getting started guide."""

    render_section_header("📚 Getting Started")

    st.markdown(
        """
        1. Open **Settings** and configure an AI model.

        2. Navigate to **Analyze Paper**.

        3. Upload a research paper (PDF).

        4. Review the generated analysis.

        5. Access previous analyses from **History**.
        """
    )


def _render_footer() -> None:
    """Render page footer."""

    render_divider()

    st.caption("Happy Researching! 🚀")


# =============================================================================
# Public API
# =============================================================================

def show_dashboard_page() -> None:
    """
    Render the Dashboard page.
    """

    _render_header()

    _render_welcome()

    _render_quick_actions()

    _render_statistics()

    _render_getting_started()

    _render_footer()