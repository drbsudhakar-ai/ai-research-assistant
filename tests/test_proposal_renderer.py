from app.models.research_project import ResearchProposal
from app.reports.proposal_renderer import (
    render_proposal_html,
    render_proposal_markdown,
    render_proposal_pdf,
)


def _proposal() -> ResearchProposal:
    return ResearchProposal(
        id=1, project_id=1, synthesis_id=1, title="Secure Collaborative Detection",
        proposal_type="Research Project", provider="gemini", model="flash", version=2,
        content="# Proposed Title\nSecure Collaborative Detection\n\n## Problem Statement\nA test problem.",
    )


def test_proposal_exports_are_branded_and_valid() -> None:
    proposal = _proposal()
    assert "AI Research Assistant" in render_proposal_markdown(proposal)
    assert "<html" in render_proposal_html(proposal).lower()
    pdf = render_proposal_pdf(proposal)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
