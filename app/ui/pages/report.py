"""
===============================================================================
Project      : AI Research Assistant
File         : report.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Report page for displaying a completed AI research paper analysis.

Responsibilities:
    - Display a previously generated analysis report.
    - Display paper metadata.
    - Display AI-generated analysis.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from app.config.branding import get_brand_config
from app.models.analysis_record import AnalysisRecord
from app.ui.components.analyze.report_export import render_report_export
from app.ui.components.page import render_page_header
from app.ui.html_renderer import render_html
from html import escape


def show_report_page() -> None:
    """
    Render the Analysis Report page.
    """

    brand = get_brand_config()
    render_page_header(
        f"{brand.icon} Analysis Report",
        "Evidence-aware research findings, paper metadata, and export-ready output.",
    )

    record: AnalysisRecord | None = st.session_state.get("analysis_record")
    if record is None:
        selected = st.session_state.get("selected_record")
        if isinstance(selected, AnalysisRecord):
            record = selected
        elif isinstance(selected, dict):
            record = AnalysisRecord.from_dict(selected)

    if record is None:
        st.info(
            "No analysis report is available.\n\n"
            "Analyze a research paper or open a report from the "
            "History page."
        )
        return

    st.success("Analysis report loaded successfully.")

    st.divider()

    render_html(f'<div class="ara-report-title">{escape(record.title)}</div>')
    st.caption(f"Source file: {record.filename}")

    metrics = st.columns(3)
    metrics[0].metric("Pages", record.total_pages)
    metrics[1].metric("Characters", f"{record.total_characters:,}")
    metrics[2].metric("Execution Time", f"{record.execution_time:.2f} sec")
    details = st.columns(3)
    details[0].metric("Analysis Type", record.analysis_type or "Paper Analysis")
    details[1].metric("Provider", record.provider.title())
    details[2].metric("Model", record.model)

    st.divider()

    st.subheader("Proposal Intelligence")
    gap_col, future_col = st.columns(2)
    with gap_col:
        st.markdown("#### Main Research Gap")
        st.info(record.research_gap or "No separate research gap was extracted.")
    with future_col:
        st.markdown("#### Future Scope")
        st.info(record.future_scope or "No separate future scope was extracted.")

    st.divider()

    st.subheader("AI Analysis")
    with st.container(border=True):
        st.markdown(record.analysis)

    render_report_export(
        {
            "title": record.title,
            "filename": record.filename,
            "pages": record.total_pages,
            "characters": record.total_characters,
            "provider": record.provider,
            "model": record.model,
            "analysis": record.analysis,
            "research_gap": record.research_gap,
            "future_scope": record.future_scope,
        }
    )

    st.divider()

    st.caption(
        f"{brand.application_name}. {brand.credit}."
    )
