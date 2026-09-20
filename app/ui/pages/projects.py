from __future__ import annotations

import streamlit as st

from app.services.service_container import ServiceContainer
from app.ui.components.page import render_page_header


def _project_label(project) -> str:
    return f"{project.name} · {project.research_domain or 'General research'}"


def show_projects_page() -> None:
    render_page_header(
        "🔬 Research Projects",
        "Compare analyzed papers, preserve consolidated gaps, and develop evidence-led proposal directions.",
    )
    container = ServiceContainer()
    repository = container.research_project_repository
    service = container.research_project_service

    with st.expander("Create a research project", expanded=not repository.list_all()):
        with st.form("create_research_project", clear_on_submit=True):
            name = st.text_input("Project name", placeholder="e.g. Collaborative intrusion detection")
            domain = st.text_input("Research domain", placeholder="e.g. Cybersecurity and machine learning")
            objective = st.text_area(
                "Research objective",
                placeholder="What should this group of papers help you investigate?",
            )
            if st.form_submit_button("Create project", type="primary", use_container_width=True):
                try:
                    service.create(name, domain, objective)
                    st.success("Research project created.")
                    st.rerun()
                except ValueError as exc:
                    st.warning(str(exc))

    projects = repository.list_all()
    if not projects:
        st.info("Create a project, then attach two or more completed paper analyses.")
        return

    project = st.selectbox("Active project", projects, format_func=_project_label)
    st.caption(project.objective or "No research objective has been recorded yet.")

    papers = repository.get_papers(project.id)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Papers", len(papers))
    metric_columns[1].metric("Saved synthesis", "Yes" if repository.latest_synthesis(project.id) else "No")
    metric_columns[2].metric("Status", project.status.title())

    all_analyses = container.history_service.get_all_analyses()
    linked_ids = {paper.id for paper in papers}
    available = [record for record in all_analyses if record.id not in linked_ids]
    with st.container(border=True):
        st.subheader("Add analyzed papers")
        if available:
            selected = st.multiselect(
                "Select completed analyses",
                available,
                format_func=lambda record: f"{record.title} · {record.provider}/{record.model}",
            )
            if st.button("Add selected papers", disabled=not selected, use_container_width=True):
                added = repository.add_papers(project.id, [item.id for item in selected])
                st.success(f"Added {added} paper(s). Duplicate links were ignored.")
                st.rerun()
        else:
            st.info("No additional completed analyses are available. Analyze another paper first.")

    st.subheader("Evidence set")
    if papers:
        for number, paper in enumerate(papers, 1):
            with st.expander(f"{number}. {paper.title}"):
                st.markdown("**Main research gap**")
                st.write(paper.research_gap or "Not separately identified.")
                st.markdown("**Future scope**")
                st.write(paper.future_scope or "Not separately identified.")
    else:
        st.info("No papers have been added to this project.")

    if st.button(
        "Generate comparative research synthesis",
        type="primary",
        disabled=len(papers) < 2,
        use_container_width=True,
    ):
        with st.spinner("Comparing evidence and identifying cross-paper gaps..."):
            try:
                service.synthesize(project)
                st.success("Comparative synthesis saved to this project.")
                st.rerun()
            except Exception as exc:  # noqa: BLE001 - friendly page boundary
                st.error(f"Synthesis could not be completed: {exc}")

    synthesis = repository.latest_synthesis(project.id)
    if synthesis:
        st.subheader("Latest comparative synthesis")
        gaps = st.columns(2)
        with gaps[0]:
            st.markdown("#### Consolidated research gap")
            st.info(synthesis.consolidated_gap or "See the complete synthesis below.")
        with gaps[1]:
            st.markdown("#### Future scope")
            st.info(synthesis.future_scope or "See the complete synthesis below.")
        with st.container(border=True):
            st.markdown(synthesis.synthesis)
        st.download_button(
            "Download synthesis (Markdown)",
            data=synthesis.synthesis,
            file_name=f"research-project-{project.id}-synthesis.md",
            mime="text/markdown",
            use_container_width=True,
        )
