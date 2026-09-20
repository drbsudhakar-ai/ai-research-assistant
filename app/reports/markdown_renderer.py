"""Markdown report renderer. Independent of Streamlit."""

from __future__ import annotations

from app.reports.report_document import ReportDocument


def render_markdown_report(document: ReportDocument) -> str:
    brand = document.resolved_brand()
    return (
        f"# {brand.application_name}\n"
        f"## {brand.document_title}\n\n"
        f"**Paper:** {document.paper_title}\n\n"
        f"{brand.credit}\n"
        f"Generated: {document.generated_label()}\n\n"
        "---\n\n"
        "## Paper Information\n\n"
        f"- Filename: {document.filename}\n"
        f"- Pages: {document.pages}\n"
        f"- Characters: {document.characters}\n"
        f"- Provider: {document.provider}\n"
        f"- Model: {document.model}\n\n"
        "---\n\n"
        "## Proposal Intelligence\n\n"
        "### Main Research Gap\n\n"
        f"{document.research_gap or 'Not separately identified.'}\n\n"
        "### Future Scope\n\n"
        f"{document.future_scope or 'Not separately identified.'}\n\n"
        "---\n\n"
        "## Analysis\n\n"
        f"{document.analysis}\n"
    )
