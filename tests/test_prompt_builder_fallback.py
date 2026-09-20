"""Regression coverage for PDFs without detectable academic headings."""

from app.models.paper_sections import PaperSections
from app.models.prepared_paper import PreparedPaper
from app.prompts.prompt_builder import PromptBuilder


def test_prompt_builder_uses_full_text_when_sections_are_not_detected() -> None:
    body = "Continuous manuscript content without standalone headings. " * 30
    paper = PreparedPaper(
        title="Unstructured Paper",
        title_source="metadata",
        title_confidence=0.9,
        filename="paper.pdf",
        text=body,
        total_pages=3,
        total_characters=len(body),
        sections=PaperSections(),
    )

    prompt = PromptBuilder().build(paper)

    assert "# Full Paper Text" in prompt
    assert body[:500] in prompt
