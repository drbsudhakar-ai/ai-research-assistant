"""
app/ui/pages/settings.py

Main Settings page controller.

Provides:
- Settings navigation
- Section routing
- Page layout

All settings implementations live in:

    app/ui/components/settings/

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from app.config.branding import get_brand_config
import streamlit as st


from app.ui.components.settings.api import (
    render_api_settings,
)
from app.ui.components.page import render_page_header
from app.ui.html_renderer import render_html



# ============================================================================
# Page Metadata
# ============================================================================

PAGE_TITLE = "Settings"

PAGE_ICON = "⚙️"



# ============================================================================
# Main Page Renderer
# ============================================================================


def render_settings_page() -> None:
    """
    Render complete Settings page.
    """

    render_header()


    selected_section = render_navigation()


    st.divider()


    render_selected_section(
        selected_section
    )



# ============================================================================
# Header
# ============================================================================


def render_header() -> None:
    """
    Render settings page header.
    """

    brand = get_brand_config()
    render_page_header(
        f"{brand.icon} Application Settings",
        "Configure AI providers, analysis workflows, reports, and workspace preferences.",
    )



# ============================================================================
# Navigation
# ============================================================================


def render_navigation() -> str:
    """
    Render settings section selector.
    """

    sections = [

        "General",

        "API Providers",

        "Pipeline",

        "Exports",

        "About",

    ]


    return st.radio(
        "Settings Section",
        sections,
        horizontal=True,
    )



# ============================================================================
# Section Router
# ============================================================================


def render_selected_section(
    section: str,
) -> None:
    """
    Route selected settings section.
    """


    if section == "General":

        render_general_settings()


    elif section == "API Providers":

        render_api_settings()


    elif section == "Pipeline":

        render_pipeline_settings()


    elif section == "Exports":

        render_export_settings()


    elif section == "About":

        render_about_section()



# ============================================================================
# Placeholder Sections
# ============================================================================


def render_general_settings() -> None:
    """
    General application settings.

    Future module:

        components/settings/general/
    """

    render_html("""<div class="ara-settings-panel"><div class="ara-settings-panel-title">⚙️ General workspace</div><div class="ara-settings-panel-copy">Application identity, interface preferences, and research-workspace defaults. Advanced controls will be enabled in a later release.</div></div>""")



def render_pipeline_settings() -> None:
    """
    Pipeline configuration settings.

    Future module:

        components/settings/pipeline/
    """

    render_html("""<div class="ara-settings-panel"><div class="ara-settings-panel-title">🔄 Analysis pipeline</div><div class="ara-settings-panel-copy">Validation, extraction, AI analysis, history persistence, and report generation are managed by the verified canonical pipeline.</div></div>""")



def render_export_settings() -> None:
    """
    Report export settings.

    Future module:

        components/settings/export/
    """

    render_html("""<div class="ara-settings-panel"><div class="ara-settings-panel-title">📄 Report exports</div><div class="ara-settings-panel-copy">Markdown, plain-text, and HTML research reports are currently available from completed analyses.</div></div>""")



def render_about_section() -> None:
    """
    About application section.
    """

    st.subheader(
        "ℹ️ About"
    )


    brand = get_brand_config()
    st.markdown(
        f"""
        ### {brand.application_name}

        A modular research intelligence platform
        for academic paper analysis.

        {brand.credit}

        Features:

        - AI-powered paper analysis
        - LLM provider abstraction
        - Research pipeline orchestration
        - History management
        """
    )



# ============================================================================
# Public Export
# ============================================================================


__all__ = [
    "render_settings_page",
]


# ============================================================================
# Backward Compatibility Entry Point
# ============================================================================

def show_settings_page() -> None:
    """
    Navigation entry point.

    Maintains compatibility with app.core.navigation.
    """

    render_settings_page()
