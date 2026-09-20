"""
===============================================================================
Project      : AI Research Assistant
File         : about.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
About page.

Responsibilities:
    - Display application information.
    - Display project details.
    - Display author information.
    - Display technology and architecture overview.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations


import streamlit as st
from app.ui.html_renderer import render_html

from app.config.branding import get_brand_config
from app.ui.components.page import (
    render_page_header,
    render_section_header,
    render_divider,
)


__all__ = [
    "show_about_page",
]


# =============================================================================
# Private Render Functions
# =============================================================================


def _render_header() -> None:
    """Render page header."""

    brand = get_brand_config()
    render_page_header(
        title=f"{brand.icon} About",
        description=(
            f"{brand.application_name} • Version {brand.version}"
        ),
    )



def _render_overview() -> None:
    """Render project overview."""

    brand = get_brand_config()
    render_html(f"""
        <div class="ara-settings-panel">
          <div class="ara-settings-panel-title">Research intelligence made practical</div>
          <div class="ara-settings-panel-copy">{brand.application_name} helps academic users extract, understand, evaluate, and report the central contributions of research papers through a governed AI-analysis workflow.</div>
        </div>
    """)



def _render_features() -> None:
    """Render application features."""

    render_section_header("Core Capabilities")
    render_html("""
      <div class="ara-info-grid">
        <div class="ara-info-card"><h3>📄 Paper intelligence</h3><p>Validated PDF extraction, section awareness, structured summaries, methodology and limitation analysis.</p></div>
        <div class="ara-info-card"><h3>🤖 Provider flexibility</h3><p>Fast Gemini cloud analysis with a provider-neutral boundary and optional private local inference.</p></div>
        <div class="ara-info-card"><h3>📚 Research continuity</h3><p>Persistent analysis history, record retrieval, reanalysis workflow, and execution metadata.</p></div>
        <div class="ara-info-card"><h3>📤 Professional outputs</h3><p>Export-ready Markdown, text, and HTML reports built from structured analysis results.</p></div>
      </div>
    """)



def _render_application_information() -> None:
    """Render application metadata."""

    render_section_header(
        "Application Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Application",
            get_brand_config().application_name,
        )


    with col2:

        st.metric(
            "Version",
            get_brand_config().version,
        )



def _render_architecture() -> None:
    """Render architecture overview."""

    render_section_header(
        "System Architecture"
    )

    render_html("""
      <div class="ara-settings-panel">
        <div class="ara-settings-panel-title">Modular analysis architecture</div>
        <div class="ara-settings-panel-copy">Streamlit Workspace → Analysis Service → Validation & Preparation Pipeline → AI Provider → History Storage → Report Renderers</div>
        <div style="margin-top:.75rem"><span class="ara-chip">PDF validation</span><span class="ara-chip">Text extraction</span><span class="ara-chip">Gemini/Ollama</span><span class="ara-chip">SQLite history</span><span class="ara-chip">Versioned reports</span></div>
      </div>
    """)



def _render_technology_stack() -> None:
    """Render technology stack."""

    render_section_header(
        "Technology Stack"
    )

    render_html("""<div><span class="ara-chip">Python</span><span class="ara-chip">Streamlit</span><span class="ara-chip">Gemini</span><span class="ara-chip">Ollama</span><span class="ara-chip">PyMuPDF</span><span class="ara-chip">SQLite</span><span class="ara-chip">HTTPX</span></div>""")



def _render_author_information() -> None:
    """Render author information."""

    render_section_header(
        "Author"
    )

    st.write(
        get_brand_config().credit
    )



def _render_footer() -> None:
    """Render footer."""

    render_divider()

    st.caption(
        get_brand_config().credit
    )



# =============================================================================
# Public Page Function
# =============================================================================


def show_about_page() -> None:
    """
    Display About page.
    """

    _render_header()

    _render_overview()

    _render_features()

    _render_application_information()

    _render_architecture()

    _render_technology_stack()

    _render_author_information()

    _render_footer()



# =============================================================================
# Streamlit Entry Point
# =============================================================================


def main() -> None:
    """Streamlit page entry point."""

    st.set_page_config(
        page_title="About",
        page_icon="ℹ️",
        layout="wide",
    )

    show_about_page()



if __name__ == "__main__":

    main()
