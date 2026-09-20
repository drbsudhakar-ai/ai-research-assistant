"""HTML report renderer. Independent of Streamlit."""

from __future__ import annotations

from html import escape

from app.reports.report_document import ReportDocument


def render_html_report(document: ReportDocument) -> str:
    brand = document.resolved_brand()
    title = escape(brand.application_name)
    report_title = escape(brand.document_title)
    paper = escape(document.paper_title)
    credit = escape(brand.credit)
    generated = escape(document.generated_label())
    analysis = escape(document.analysis)
    research_gap = escape(document.research_gap or "Not separately identified.")
    future_scope = escape(document.future_scope or "Not separately identified.")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} — {report_title}</title>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <h2>{report_title}</h2>
    <p><strong>Paper:</strong> {paper}</p>
    <p>{credit}<br>Generated: {generated}</p>
  </header>
  <main>
    <h3>Paper Information</h3>
    <ul>
      <li>Filename: {escape(str(document.filename))}</li>
      <li>Pages: {escape(str(document.pages))}</li>
      <li>Characters: {escape(str(document.characters))}</li>
      <li>Provider: {escape(str(document.provider))}</li>
      <li>Model: {escape(str(document.model))}</li>
    </ul>
    <h3>Proposal Intelligence</h3>
    <h4>Main Research Gap</h4>
    <p>{research_gap}</p>
    <h4>Future Scope</h4>
    <pre>{future_scope}</pre>
    <h3>Analysis</h3>
    <pre>{analysis}</pre>
  </main>
  <footer>
    <p>{title} · {credit}</p>
  </footer>
</body>
</html>
"""
