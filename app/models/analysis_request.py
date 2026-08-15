"""Canonical analysis request.

This is an input identity contract. It does not execute analysis, read
PDFs, or depend on Streamlit upload objects.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.exceptions import DomainValidationError

__all__ = ["AnalysisRequest"]

DEFAULT_ANALYSIS_TYPE = "Research Paper Analysis"


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    """Request to analyze a research paper already available as a path identity."""

    source_path: str
    filename: str = ""
    analysis_type: str = DEFAULT_ANALYSIS_TYPE

    def __post_init__(self) -> None:
        path = str(self.source_path).strip()
        if not path:
            raise DomainValidationError(
                "source_path is required.",
                field="source_path",
            )
        object.__setattr__(self, "source_path", path)
        name = str(self.filename).strip() or path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        object.__setattr__(self, "filename", name)
        analysis_type = str(self.analysis_type).strip() or DEFAULT_ANALYSIS_TYPE
        object.__setattr__(self, "analysis_type", analysis_type)

    def to_dict(self) -> dict[str, str]:
        return {
            "source_path": self.source_path,
            "filename": self.filename,
            "analysis_type": self.analysis_type,
        }
