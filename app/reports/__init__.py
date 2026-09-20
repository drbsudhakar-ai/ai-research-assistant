"""Streamlit-independent report generation."""

from app.reports.html_renderer import render_html_report
from app.reports.markdown_renderer import render_markdown_report
from app.reports.report_document import ReportDocument

__all__ = [
    "ReportDocument",
    "render_html_report",
    "render_markdown_report",
]
