from __future__ import annotations

from app.models.research_project import ResearchProject, ResearchProposal, ResearchSynthesis
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

PROPOSAL_SYSTEM_PROMPT = """You are an academic research proposal writer. Use only the
provided synthesis and evidence list. Do not invent references, findings, datasets,
funding details, or institutional approvals. Clearly label assumptions. Produce polished
markdown. This is a researcher-owned working draft: do not claim it is human-authored,
do not optimize for AI-detector evasion, and do not reproduce source wording without
quotation and attribution. Use these exact sections:
# Proposed Title
## Abstract
## Background and Rationale
## Problem Statement
## Main Research Gap
## Aim
## Research Objectives
## Research Questions
## Proposed Methodology
## Expected Outcomes
## Innovation and Significance
## Scope and Limitations
## Ethical and Data Considerations
## Work Plan and Timeline
## Evidence Traceability
## References to Source Papers
"""

POSTDOCTORAL_REQUIREMENTS = """For a Post-Doctoral Fellowship Proposal, also include:
## Applicant Research Background
## Connection with Doctoral Research
## Host Institution and Mentor Fit
## Fellowship Deliverables
## Fellowship Duration and Milestones
## Facilities and Resources Required
## Career Development Contribution
Use supplied applicant/host details only. Mark missing details as 'To be completed by applicant'.
"""

PROJECT_REQUIREMENTS = """For a Research Project Proposal, also include:
## Project Team and Institutional Capacity
## Project Deliverables
## Budget Heads and Justification
## Implementation and Dissemination Plan
Do not invent team, institution, or budget figures. Mark missing details for researcher completion.
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

    def generate_proposal(
        self,
        project: ResearchProject,
        proposal_type: str = "Research Project",
        title_guidance: str = "",
        applicant_context: str = "",
    ) -> ResearchProposal:
        if project.id is None:
            raise ValueError("Project must be saved before proposal generation.")
        synthesis = self.repository.latest_synthesis(project.id)
        if synthesis is None or synthesis.id is None:
            raise ValueError("Generate a comparative synthesis before creating a proposal.")
        papers = self.repository.get_papers(project.id)
        evidence = "\n".join(
            f"- Source {index}: {paper.title} ({paper.filename})"
            for index, paper in enumerate(papers, 1)
        )
        prompt = (
            f"Proposal type: {proposal_type}\nProject: {project.name}\n"
            f"Domain: {project.research_domain}\nObjective: {project.objective}\n"
            f"Title guidance: {title_guidance or 'Develop the strongest evidence-led title.'}\n\n"
            f"APPLICANT / HOST / SCHEME CONTEXT\n"
            f"{applicant_context or 'Not supplied; mark applicant-specific fields for completion.'}\n\n"
            f"COMPARATIVE SYNTHESIS\n{synthesis.synthesis}\n\n"
            f"SOURCE PAPERS\n{evidence}"
        )
        type_requirements = (
            POSTDOCTORAL_REQUIREMENTS
            if proposal_type == "Post-Doctoral Fellowship Proposal"
            else PROJECT_REQUIREMENTS
        )
        response = self.llm.generate(
            system_prompt=f"{PROPOSAL_SYSTEM_PROMPT}\n{type_requirements}",
            user_prompt=prompt,
        )
        title = self._extract_proposal_title(response.content, project.name)
        proposal = ResearchProposal(
            project_id=project.id,
            synthesis_id=synthesis.id,
            title=title,
            proposal_type=proposal_type,
            content=response.content,
            provider=response.provider,
            model=response.model,
        )
        proposal.id = self.repository.save_proposal(proposal)
        return proposal

    @staticmethod
    def _extract_proposal_title(content: str, fallback: str) -> str:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        for index, line in enumerate(lines):
            if line.casefold() in {"# proposed title", "proposed title"} and index + 1 < len(lines):
                return lines[index + 1].lstrip("#* ").strip() or fallback
            if line.startswith("# ") and line.casefold() != "# proposed title":
                return line[2:].strip() or fallback
        return fallback
