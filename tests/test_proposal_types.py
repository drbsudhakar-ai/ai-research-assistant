from pathlib import Path

from app.services.research_project_service import (
    POSTDOCTORAL_REQUIREMENTS,
    PROJECT_REQUIREMENTS,
    PROPOSAL_SYSTEM_PROMPT,
)


def test_postdoctoral_fellowship_requirements_are_explicit() -> None:
    assert "Post-Doctoral Fellowship Proposal" in POSTDOCTORAL_REQUIREMENTS
    assert "Connection with Doctoral Research" in POSTDOCTORAL_REQUIREMENTS
    assert "Host Institution and Mentor Fit" in POSTDOCTORAL_REQUIREMENTS
    assert "Fellowship Duration and Milestones" in POSTDOCTORAL_REQUIREMENTS


def test_project_requirements_do_not_invent_budget() -> None:
    assert "Budget Heads and Justification" in PROJECT_REQUIREMENTS
    assert "Do not invent" in PROJECT_REQUIREMENTS


def test_prompt_enforces_research_integrity() -> None:
    assert "do not optimize for AI-detector evasion" in PROPOSAL_SYSTEM_PROMPT
    assert "quotation and attribution" in PROPOSAL_SYSTEM_PROMPT


def test_ui_uses_full_postdoctoral_term() -> None:
    source = Path("app/ui/pages/projects.py").read_text(encoding="utf-8")
    assert "Post-Doctoral Fellowship Proposal" in source
    assert '"PDF Proposal"' not in source
