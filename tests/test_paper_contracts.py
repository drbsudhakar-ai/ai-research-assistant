"""PaperSections and preparation contract tests."""

from __future__ import annotations

import inspect

import pytest

from app.models.paper_sections import PaperSections
from app.models.prepared_paper import PreparedPaper


def test_paper_sections_count_and_len() -> None:
    empty = PaperSections()
    assert empty.section_count == 0
    assert len(empty) == 0
    assert empty.is_empty

    sections = PaperSections(
        abstract="An abstract.",
        introduction="An introduction.",
    )
    assert sections.section_count == 2
    assert len(sections) == 2
    assert "Abstract" in sections.available_sections


def test_prepared_paper_requires_sections() -> None:
    signature = inspect.signature(PreparedPaper)
    assert "sections" in signature.parameters


def test_pdf_extractor_contract() -> None:
    pytest.importorskip("fitz")
    from app.utils.pdf_extractor import PDFExtractor

    assert hasattr(PDFExtractor, "extract_text")
    signature = inspect.signature(PDFExtractor.extract_text)
    assert "file" in signature.parameters


def test_preprocessor_prepare_signature() -> None:
    pytest.importorskip("fitz")
    from app.utils.paper_preprocessor import PaperPreprocessor

    signature = inspect.signature(PaperPreprocessor.prepare)
    assert "extracted" in signature.parameters
    assert "filename" in signature.parameters
