"""
===============================================================================
Project      : AI Research Assistant
File         : about.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
About page.

Responsibilities:
    - Display application information.
    - Display project details.
    - Display author information.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from app.config.app_config import (
    APP_NAME,
    APP_VERSION,
    AUTHOR,
)

from app.ui.components.page import (
    render_page_header,
    render_section_header,
    render_divider,
)

__all__ = [
    "show_about_page",
]


def _render_header() -> None:
    render_page_header(
        title="ℹ️ About",
        description=f"{APP_NAME} • Version {APP_VERSION}",
    )


    
def _render_overview() -> None:
    """Render the project overview."""

    render_section_header("Project Overview")

    st.write(
        """
        AI Research Assistant is a Streamlit-based application designed to
        help researchers analyze academic papers using Large Language Models.

        The application streamlines literature review by generating summaries,
        extracting keywords, identifying research gaps, and providing
        actionable insights.
        """
    )
    
def _render_features() -> None:
    """Render application features."""

    render_section_header("Key Features")

    st.markdown(
        """
        - 📄 PDF paper analysis
        - 🤖 AI-powered summarization
        - 🔍 Keyword extraction
        - 💡 Research gap identification
        - 🕒 Analysis history
        - ⚙️ Configurable AI models
        """
    )


def _render_application_information() -> None:
    """Render application information."""

    render_section_header("Application")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Application", APP_NAME)

    with col2:
        st.metric("Version", APP_VERSION)


def _render_technology_stack() -> None:
    """Render technology stack."""

    render_section_header("Technology Stack")

    st.markdown(
        """
        - Python
        - Streamlit
        - LangChain
        - Ollama
        - Google Gemini
        - PyMuPDF
        """
    )

def _render_author_information() -> None:
    """Render author information."""

    render_section_header("Author")

    st.write(AUTHOR)

def _render_footer() -> None:
    """Render footer."""

    render_divider()

    st.caption(f"Developed by {AUTHOR}")
    
    
def show_about_page() -> None:
    """Display the About page."""

    _render_header()

    _render_overview()

    _render_features()

    _render_application_information()

    _render_technology_stack()

    _render_author_information()

    _render_footer()