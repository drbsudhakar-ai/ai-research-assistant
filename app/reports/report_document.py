"""Structured report data consumed by format renderers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.config.branding import BrandConfig, get_brand_config
from app.models.analysis_record import AnalysisRecord
from app.models.analysis_result import AnalysisResult


@dataclass(frozen=True, slots=True)
class ReportDocument:
    """Brand-aware payload for downloadable analysis reports.

    This module does not render Markdown/HTML/PDF.
    """

    paper_title: str
    analysis: str
    filename: str = ""
    pages: int | str = "-"
    characters: int | str = "-"
    provider: str = ""
    model: str = ""
    generated_at: datetime | None = None
    brand: BrandConfig | None = None

    def resolved_brand(self) -> BrandConfig:
        return self.brand or get_brand_config()

    def generated_label(self) -> str:
        moment = self.generated_at or datetime.now(timezone.utc).astimezone()
        return moment.strftime("%Y-%m-%d %H:%M")

    @classmethod
    def from_mapping(
        cls,
        record: dict[str, Any],
        *,
        brand: BrandConfig | None = None,
    ) -> ReportDocument:
        analysis = record.get("analysis") or record.get("content") or ""
        return cls(
            paper_title=str(record.get("title") or "Untitled Paper"),
            analysis=str(analysis),
            filename=str(record.get("filename") or "-"),
            pages=record.get("pages", record.get("total_pages", "-")),
            characters=record.get(
                "characters",
                record.get("total_characters", "-"),
            ),
            provider=str(record.get("provider") or "-"),
            model=str(record.get("model") or "-"),
            brand=brand,
        )

    @classmethod
    def from_result(
        cls,
        result: AnalysisResult,
        *,
        title: str = "Untitled Paper",
        filename: str = "-",
        pages: int | str = "-",
        characters: int | str = "-",
        brand: BrandConfig | None = None,
    ) -> ReportDocument:
        return cls(
            paper_title=title,
            analysis=result.analysis,
            filename=filename,
            pages=pages,
            characters=characters,
            provider=result.provider,
            model=result.model,
            brand=brand,
        )

    @classmethod
    def from_record(
        cls,
        record: AnalysisRecord,
        *,
        brand: BrandConfig | None = None,
    ) -> ReportDocument:
        return cls.from_mapping(record.to_dict(), brand=brand)
