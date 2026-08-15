"""Report renderer tests."""

from __future__ import annotations

from app.config.branding import get_brand_config
from app.reports import (
    ReportDocument,
    render_html_report,
    render_markdown_report,
)


def test_markdown_and_html_include_branding() -> None:
    brand = get_brand_config()
    document = ReportDocument.from_mapping(
        {
            "title": "Sample Paper",
            "filename": "sample.pdf",
            "pages": 4,
            "characters": 1200,
            "provider": "ollama",
            "model": "qwen3:4b",
            "analysis": "Findings go here.",
        },
        brand=brand,
    )
    markdown = render_markdown_report(document)
    html = render_html_report(document)
    for payload in (markdown, html):
        assert brand.application_name in payload
        assert brand.document_title in payload
        assert "Sample Paper" in payload
        assert brand.credit in payload
        assert "Generated:" in payload


def test_html_escapes_untrusted_content() -> None:
    document = ReportDocument.from_mapping(
        {
            "title": "<script>x</script>",
            "analysis": "<b>raw</b>",
        }
    )
    html = render_html_report(document)
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;x&lt;/script&gt;" in html
