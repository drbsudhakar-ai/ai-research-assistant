"""Canonical provider-neutral analysis outcome.

This is not a history row, not a pipeline envelope, and not an LLM SDK
response. ``LLMResponse`` is the raw provider output; ``AnalysisResult``
is the application-facing analysis product.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.models.analysis_status import AnalysisStatus
from app.models.exceptions import DomainValidationError
from app.models.llm_response import LLMResponse
from app.utils.research_insights import extract_research_insights

__all__ = ["AnalysisResult"]


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Completed analysis content plus provider metadata."""

    analysis: str
    provider: str
    model: str
    execution_time: float = 0.0
    status: AnalysisStatus = AnalysisStatus.COMPLETED
    research_gap: str = ""
    future_scope: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.analysis, str) or not self.analysis.strip():
            raise DomainValidationError(
                "analysis content is required.",
                field="analysis",
            )
        if not str(self.provider).strip():
            raise DomainValidationError("provider is required.", field="provider")
        if not str(self.model).strip():
            raise DomainValidationError("model is required.", field="model")
        if self.execution_time < 0:
            raise DomainValidationError(
                "execution_time cannot be negative.",
                field="execution_time",
            )
        if not isinstance(self.status, AnalysisStatus):
            try:
                object.__setattr__(self, "status", AnalysisStatus(str(self.status)))
            except ValueError as exc:
                raise DomainValidationError(
                    f"Invalid analysis status: {self.status!r}.",
                    field="status",
                ) from exc

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AnalysisResult:
        payload = dict(data)
        if "status" in payload and not isinstance(payload["status"], AnalysisStatus):
            payload["status"] = AnalysisStatus(payload["status"])
        return cls(**payload)

    @classmethod
    def from_llm_response(
        cls,
        response: LLMResponse,
        *,
        execution_time: float = 0.0,
        status: AnalysisStatus = AnalysisStatus.COMPLETED,
    ) -> AnalysisResult:
        research_gap, future_scope = extract_research_insights(response.content)
        return cls(
            analysis=response.content,
            provider=response.provider,
            model=response.model,
            execution_time=execution_time,
            status=status,
            research_gap=research_gap,
            future_scope=future_scope,
        )

    @classmethod
    def from_record(cls, record: Any) -> AnalysisResult:
        """Adapt a history ``AnalysisRecord`` into the result contract."""

        return cls(
            analysis=str(getattr(record, "analysis", "")),
            provider=str(getattr(record, "provider", "")),
            model=str(getattr(record, "model", "")),
            execution_time=float(getattr(record, "execution_time", 0.0) or 0.0),
            status=AnalysisStatus.COMPLETED,
            research_gap=str(getattr(record, "research_gap", "")),
            future_scope=str(getattr(record, "future_scope", "")),
        )
