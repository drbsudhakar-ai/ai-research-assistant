from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(slots=True)
class ResearchProject:
    name: str
    research_domain: str = ""
    objective: str = ""
    status: str = "active"
    id: int | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class ResearchSynthesis:
    project_id: int
    synthesis: str
    consolidated_gap: str = ""
    future_scope: str = ""
    provider: str = ""
    model: str = ""
    id: int | None = None
    created_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class ResearchProposal:
    project_id: int
    synthesis_id: int
    title: str
    proposal_type: str
    content: str
    provider: str
    model: str
    version: int = 1
    id: int | None = None
    created_at: str = field(default_factory=utc_now)
