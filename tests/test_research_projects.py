from app.models.analysis_record import AnalysisRecord
from app.models.research_project import ResearchProject, ResearchProposal, ResearchSynthesis
from app.storage.database import initialize_database
from app.storage.history_repository import HistoryRepository
from app.storage.research_project_repository import ResearchProjectRepository


def test_project_links_papers_and_retains_latest_synthesis(tmp_path, monkeypatch):
    database_path = tmp_path / "research.db"
    initialize_database(database_path)
    monkeypatch.setattr(
        "app.storage.history_repository.get_connection",
        lambda: __import__("app.storage.database", fromlist=["get_connection"]).get_connection(database_path),
    )
    history = HistoryRepository()
    ids = []
    for number in (1, 2):
        ids.append(history.add(AnalysisRecord(
            title=f"Paper {number}", filename=f"paper-{number}.pdf",
            input_source="PDF", analysis_type="Research Paper Analysis",
            analysis="Analysis", research_gap="Gap", future_scope="Scope",
            provider="gemini", model="flash",
        )))

    repository = ResearchProjectRepository(database_path)
    project_id = repository.create(ResearchProject(name="Test Project"))
    assert repository.add_papers(project_id, ids) == 2
    assert repository.add_papers(project_id, ids) == 0
    assert [paper.title for paper in repository.get_papers(project_id)] == ["Paper 2", "Paper 1"]
    assert repository.linked_filenames(project_id) == {"paper-1.pdf", "paper-2.pdf"}

    synthesis = ResearchSynthesis(
        project_id=project_id, synthesis="Report", consolidated_gap="Gap A",
        future_scope="Scope A", provider="gemini", model="flash",
    )
    repository.save_synthesis(synthesis)
    saved = repository.latest_synthesis(project_id)
    assert saved is not None
    assert saved.consolidated_gap == "Gap A"

    proposal = ResearchProposal(
        project_id=project_id, synthesis_id=saved.id, title="Proposal A",
        proposal_type="Research Project", content="# Proposed Title\nProposal A",
        provider="gemini", model="flash",
    )
    repository.save_proposal(proposal)
    repository.save_proposal(ResearchProposal(
        project_id=project_id, synthesis_id=saved.id, title="Proposal B",
        proposal_type="Research Project", content="# Proposed Title\nProposal B",
        provider="gemini", model="flash",
    ))
    proposals = repository.list_proposals(project_id)
    assert [item.version for item in proposals] == [2, 1]
