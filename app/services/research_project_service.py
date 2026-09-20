from __future__ import annotations

from app.models.research_project import ResearchProject, ResearchSynthesis
from app.services.llm_service import LLMService
from app.storage.research_project_repository import ResearchProjectRepository
from app.utils.research_insights import extract_research_insights


SYSTEM_PROMPT = """You are a rigorous research synthesis assistant. Compare only the
evidence supplied. Do not invent citations or claims. Clearly separate evidence,
limitations, and proposed work. Return markdown with these exact headings:
## Cross-Paper Findings
## Agreements and Contradictions
## Evidence and Method Limitations
### Main Research Gap
### Future Scope
## Ranked Proposal Directions
## Recommended Next Study
"""


class ResearchProjectService:
    def __init__(self, repository: ResearchProjectRepository, llm: LLMService) -> None:
        self.repository = repository
        self.llm = llm

    def create(self, name: str, domain: str, objective: str) -> int:
        if not name.strip():
            raise ValueError("Project name is required.")
        return self.repository.create(
            ResearchProject(name=name.strip(), research_domain=domain.strip(),
                            objective=objective.strip())
        )

    def synthesize(self, project: ResearchProject) -> ResearchSynthesis:
        if project.id is None:
            raise ValueError("Project must be saved before synthesis.")
        papers = self.repository.get_papers(project.id)
        if len(papers) < 2:
            raise ValueError("Add at least two analyzed papers to compare.")
        blocks = []
        for index, paper in enumerate(papers, 1):
            blocks.append(
                f"PAPER {index}\nTitle: {paper.title}\n"
                f"Research gap: {paper.research_gap or 'Not separately identified'}\n"
                f"Future scope: {paper.future_scope or 'Not separately identified'}\n"
                f"Analysis excerpt:\n{paper.analysis[:6000]}"
            )
        prompt = (
            f"Project: {project.name}\nDomain: {project.research_domain}\n"
            f"Objective: {project.objective}\n\n" + "\n\n---\n\n".join(blocks)
        )
        response = self.llm.generate(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        gap, future = extract_research_insights(response.content)
        result = ResearchSynthesis(
            project_id=project.id, synthesis=response.content,
            consolidated_gap=gap, future_scope=future,
            provider=response.provider, model=response.model,
        )
        result.id = self.repository.save_synthesis(result)
        return result
