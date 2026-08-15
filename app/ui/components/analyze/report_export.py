"""
Report export UI component.

Generation lives in app.reports (no Streamlit).
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from app.reports import (
    ReportDocument,
    render_html_report,
    render_markdown_report,
)


def render_report_export(
    record: dict[str, Any] | None,
) -> None:
    if not record:
        return

    document = ReportDocument.from_mapping(record)
    if not document.analysis:
        return

    st.divider()
    st.subheader("⬇ Export Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Markdown",
            data=create_markdown(record),
            file_name="research_analysis.md",
            mime="text/markdown",
        )

    with col2:
        st.download_button(
            label="Text",
            data=document.analysis,
            file_name="research_analysis.txt",
            mime="text/plain",
        )

    with col3:
        st.download_button(
            label="HTML",
            data=create_html(record),
            file_name="research_analysis.html",
            mime="text/html",
        )


def create_markdown(record: dict[str, Any]) -> str:
    return render_markdown_report(ReportDocument.from_mapping(record))


def create_html(record: dict[str, Any]) -> str:
    return render_html_report(ReportDocument.from_mapping(record))
