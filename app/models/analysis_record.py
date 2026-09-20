"""
===============================================================================
Project      : AI Research Assistant
File         : analysis_record.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
History/application contract for a completed research paper analysis.

This is persistence-oriented identity plus result payload. It is not a
SQLite row type and contains no SQL.

``AnalysisResult`` is the canonical analysis-outcome contract. Use
``to_result()`` / ``from_result()`` to convert.
===============================================================================
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from app.models.analysis_result import AnalysisResult
from app.models.exceptions import DomainValidationError
from app.models.prepared_paper import PreparedPaper

__all__ = [
    "AnalysisRecord",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(slots=True)
class AnalysisRecord:
    """Completed analysis snapshot used by history services.

    ``id`` is assigned after persistence and may be mutated by repositories.
    """

    id: int | None = None
    title: str = ""
    filename: str = ""
    input_source: str = ""
    analysis_type: str = ""
    total_pages: int = 0
    total_characters: int = 0
    analysis: str = ""
    research_gap: str = ""
    future_scope: str = ""
    provider: str = ""
    model: str = ""
    execution_time: float = 0.0
    created_at: str = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if self.total_pages < 0:
            raise DomainValidationError(
                "total_pages cannot be negative.",
                field="total_pages",
            )
        if self.total_characters < 0:
            raise DomainValidationError(
                "total_characters cannot be negative.",
                field="total_characters",
            )
        if self.execution_time < 0:
            raise DomainValidationError(
                "execution_time cannot be negative.",
                field="execution_time",
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AnalysisRecord:
        return cls(**data)

    def to_result(self) -> AnalysisResult:
        return AnalysisResult.from_record(self)

    @classmethod
    def from_result(
        cls,
        result: AnalysisResult,
        *,
        paper: PreparedPaper | None = None,
        title: str = "",
        filename: str = "",
        input_source: str = "PDF",
        analysis_type: str = "Research Paper Analysis",
        total_pages: int = 0,
        total_characters: int = 0,
    ) -> AnalysisRecord:
        if paper is not None:
            title = paper.title
            filename = paper.filename
            total_pages = paper.total_pages
            total_characters = paper.total_characters
        return cls(
            title=title,
            filename=filename,
            input_source=input_source,
            analysis_type=analysis_type,
            total_pages=total_pages,
            total_characters=total_characters,
            analysis=result.analysis,
            research_gap=result.research_gap,
            future_scope=result.future_scope,
            provider=result.provider,
            model=result.model,
            execution_time=result.execution_time,
        )
