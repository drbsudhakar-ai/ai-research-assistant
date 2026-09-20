"""Extract proposal-oriented insights from a structured Markdown analysis."""

from __future__ import annotations

import re

__all__ = ["extract_research_insights"]


def _section(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def _label(markdown: str, labels: tuple[str, ...]) -> str:
    alternatives = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(
        rf"^\s*[-*]\s*\*\*(?:{alternatives}):?\*\*\s*(.+)$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def extract_research_insights(markdown: str) -> tuple[str, str]:
    """Return separately reusable main-gap and future-scope text.

    New reports use the exact Proposal Intelligence headings. Label-based
    fallbacks retain compatibility with reports created before this feature.
    """

    research_gap = _section(markdown, "Main Research Gap") or _label(
        markdown,
        ("Research Gap", "Research Gaps"),
    )
    future_scope = _section(markdown, "Future Scope") or _label(
        markdown,
        ("Future Scope", "Future Work", "Future directions"),
    )
    return research_gap, future_scope
