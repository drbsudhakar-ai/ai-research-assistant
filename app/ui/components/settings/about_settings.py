"""
app/ui/components/settings/about_settings.py

About Settings UI Component

Displays application information, project details,
technology stack, and version information for the
AI Research Assistant application.

Version:
    1.0.0

Author:
    Dr B Sudhakar

Description:
    - Application information
    - Version details
    - Architecture overview
    - Technology stack
    - Project links

This component is UI-only.
"""

from __future__ import annotations

from typing import Dict, Any

import streamlit as st


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPONENT_TITLE = "About"


APP_INFORMATION: Dict[str, Any] = {
    "name": "AI Research Assistant",
    "version": "0.4.0",
    "status": "Development",
    "author": "Dr B Sudhakar",
    "description": (
        "An intelligent research paper analysis platform "
        "using AI agents, LLMs, and modular processing pipelines."
    ),
}


TECHNOLOGY_STACK = [
    "Python",
    "Streamlit",
    "LangGraph",
    "Ollama",
    "Local LLM Models",
    "SQLite",
    "PDF Processing",
    "AI Agent Pipeline Architecture",
]


ARCHITECTURE_COMPONENTS = [
    "Document Processing Layer",
    "Paper Analysis Pipeline",
    "LLM Provider Abstraction",
    "History Storage System",
    "Report Export Framework",
    "Modular Streamlit UI",
]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_about_settings() -> None:
    """
    Render About section.

    Displays application information and
    architecture details.
    """

    st.subheader(
        COMPONENT_TITLE
    )

    st.caption(
        "Information about the AI Research Assistant project."
    )


    # ------------------------------------------------------------------
    # Application Information
    # ------------------------------------------------------------------

    st.markdown(
        "### Application Information"
    )


    st.write(
        f"""
        **Application Name:**
        {APP_INFORMATION["name"]}

        **Version:**
        {APP_INFORMATION["version"]}

        **Status:**
        {APP_INFORMATION["status"]}

        **Author:**
        {APP_INFORMATION["author"]}
        """
    )


    st.info(
        APP_INFORMATION["description"]
    )


    # ------------------------------------------------------------------
    # Technology Stack
    # ------------------------------------------------------------------

    st.markdown(
        "### Technology Stack"
    )


    for technology in TECHNOLOGY_STACK:

        st.markdown(
            f"- {technology}"
        )


    # ------------------------------------------------------------------
    # Architecture
    # ------------------------------------------------------------------

    st.markdown(
        "### System Architecture"
    )


    for component in ARCHITECTURE_COMPONENTS:

        st.markdown(
            f"- {component}"
        )


    # ------------------------------------------------------------------
    # Project Vision
    # ------------------------------------------------------------------

    st.markdown(
        "### Project Vision"
    )


    st.write(
        """
        The AI Research Assistant aims to support researchers
        by automating literature understanding, extracting
        meaningful insights, and generating structured research
        reports.

        The system follows a modular AI-agent architecture
        designed for extensibility, privacy, and future
        integration with multiple LLM providers.
        """
    )


    # ------------------------------------------------------------------
    # Development Information
    # ------------------------------------------------------------------

    st.markdown(
        "### Development"
    )


    st.code(
        """
AI Research Assistant

Architecture:
    - Modular Components
    - Pipeline-based Processing
    - Provider Independent LLM Layer
    - Persistent Analysis History
    - Extensible Export Framework
        """,
        language="text",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "render_about_settings",
]