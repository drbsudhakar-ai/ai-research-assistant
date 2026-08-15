"""Structured report data consumed by format renderers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.config.branding import BrandConfig, get_brand_config


@dataclass(frozen=True, slots=True)
class ReportDocument:
    """Brand-aware payload for downloadable analysis reports."""

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
