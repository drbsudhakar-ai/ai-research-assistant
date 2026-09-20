"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Paper Page
File         : analyze.py
Version      : 4.0.0

Description:
    Production Streamlit UI for research paper analysis.

    Features:
        - PDF upload
        - Full PDF preview
        - Background execution
        - Real pipeline progress
        - Cancellation support
        - Result rendering

===============================================================================
"""

from __future__ import annotations

import logging
import queue
import threading
from dataclasses import fields
from pathlib import Path
from queue import Empty

import streamlit as st

from app.config.branding import get_brand_config
from app.config.loader import get_application_config
from app.core.progress.progress_manager import ProgressManager
from app.core.progress.progress_renderer import ProgressRenderer
from app.models.analysis_request import AnalysisRequest
from app.models.analysis_result import AnalysisResult
from app.models.prepared_paper import PreparedPaper
from app.services.service_container import ServiceContainer
from app.ui.components.analyze.report_export import render_report_export
from app.ui.components.page import render_page_header
from app.ui.html_renderer import render_html
from app.utils.safe_filename import resolve_upload_path

_analysis_queue = queue.Queue()
_LOGGER = logging.getLogger(__name__)


__all__ = [
    "render",
    "show_analyze_page",
]


# =============================================================================
# Public Entry
# =============================================================================


def show_analyze_page() -> None:
    """
    Backward-compatible entry point.

    TODO:
        Remove after all callers migrate to render().
    """
    render()


def render() -> None:
    """
    Render Analyze Paper page.
    """

    _initialize_state()

    brand = get_brand_config()
    render_page_header(
        title=f"{brand.icon} Analyze Research Paper",
        description=brand.tagline,
    )

    container = ServiceContainer()

    _consume_reanalysis_request(container)

    _render_provider_notice(container)

    _render_upload_section(container)

    _poll_analysis()

    _render_running_analysis()


def _render_provider_notice(container: ServiceContainer) -> None:
    """Show the active provider and cloud privacy boundary."""

    provider = container.config.llm.provider
    model = container.config.llm.model
    render_html(f"""
        <div class="ara-provider-bar">
            <div>
                <div class="ara-provider-label">ACTIVE AI CONFIGURATION</div>
                <strong>Paper analysis is ready</strong>
            </div>
            <div class="ara-provider-value">● {provider.title()} · {model}</div>
        </div>
    """)
    if provider == "gemini":
        st.warning(
            "Cloud analysis sends extracted paper text to Google Gemini. "
            "Do not upload confidential, unpublished, personal, or restricted "
            "documents without authorization."
        )


# =============================================================================
# Session State
# =============================================================================


def _initialize_state() -> None:
    """
    Initialize Streamlit state.
    """

    defaults = {
        "analysis_running": False,
        "analysis_worker": None,
        "analysis_result": None,
        "analysis_error": None,
        "progress_manager": None,
        "pdf_path": None,
        "prepared_paper": None,
        "pdf_result": None,
        "reanalysis_mode": False,
        "reanalysis_source_title": "",
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =============================================================================
# Upload
# =============================================================================


def _render_upload_section(
    container: ServiceContainer,
) -> None:
    """
    Render upload controls.
    """

    if st.session_state.reanalysis_mode and st.session_state.pdf_path is not None:
        _render_reanalysis_source()
        return

    uploaded_file = st.file_uploader(
        "Upload Research Paper PDF",
        type=["pdf"],
        disabled=(st.session_state.analysis_running),
    )
    if uploaded_file is None:
        st.session_state.pdf_path = None
        st.session_state.prepared_paper = None
        st.session_state.pdf_result = None
        st.info("Upload a research paper PDF to begin analysis.")
        return

    try:
        pdf_path = _save_uploaded_file(uploaded_file)
        pdf_result = container.pdf_extractor.extract_text(uploaded_file)
        prepared_paper = container.paper_preprocessor.prepare(
            extracted=pdf_result,
            filename=uploaded_file.name,
        )
    except (ValueError, OSError) as exc:
        st.session_state.pdf_path = None
        st.session_state.prepared_paper = None
        st.session_state.pdf_result = None
        st.error(str(exc))
        return

    st.session_state.pdf_path = pdf_path
    st.session_state.prepared_paper = prepared_paper
    st.session_state.pdf_result = pdf_result
    st.success(uploaded_file.name)

    _render_paper_information(prepared_paper)

    if not st.session_state.analysis_running and st.button(
        "🚀 Analyze Paper",
        type="primary",
        disabled=(
            st.session_state.analysis_running or st.session_state.prepared_paper is None
        ),
    ):

        _start_analysis(
            container,
            st.session_state.pdf_path,
        )

    _render_pdf_preview(pdf_path)


def _consume_reanalysis_request(container: ServiceContainer) -> None:
    """Load a historical paper and begin a fresh analysis exactly once."""

    record = st.session_state.pop("reanalyze_record", None)
    if record is None:
        return

    filename = str(record.get("filename") or "").strip()
    if not filename:
        st.session_state.reanalysis_mode = False
        st.session_state.analysis_error = (
            "This older history entry does not contain its source filename. "
            "Please upload the original PDF again."
        )
        return

    try:
        pdf_path = resolve_upload_path(
            container.config.paths.uploads_dir,
            filename,
        )
    except ValueError as exc:
        st.session_state.reanalysis_mode = False
        st.session_state.analysis_error = f"The saved source filename is invalid: {exc}"
        return

    if not pdf_path.is_file():
        st.session_state.reanalysis_mode = False
        st.session_state.analysis_error = (
            f'The original PDF "{filename}" is no longer available. '
            "Please upload it again to run a fresh analysis."
        )
        return

    try:
        with pdf_path.open("rb") as pdf_file:
            pdf_result = container.pdf_extractor.extract_text(pdf_file)
        prepared_paper = container.paper_preprocessor.prepare(
            extracted=pdf_result,
            filename=filename,
        )
    except (ValueError, OSError) as exc:
        st.session_state.reanalysis_mode = False
        st.session_state.analysis_error = f"Unable to reload the original PDF: {exc}"
        return

    st.session_state.pdf_path = pdf_path
    st.session_state.pdf_result = pdf_result
    st.session_state.prepared_paper = prepared_paper
    st.session_state.reanalysis_mode = True
    st.session_state.reanalysis_source_title = str(
        record.get("title") or prepared_paper.title
    )

    _start_analysis(container, pdf_path)


def _render_reanalysis_source() -> None:
    """Render the retained source while its fresh analysis is running."""

    paper = st.session_state.prepared_paper
    pdf_path = Path(st.session_state.pdf_path)

    st.info(
        f'Fresh analysis requested for "{st.session_state.reanalysis_source_title}". '
        "The original PDF has been loaded from analysis history."
    )

    if st.button(
        "Analyze a different paper",
        disabled=st.session_state.analysis_running,
    ):
        st.session_state.reanalysis_mode = False
        st.session_state.reanalysis_source_title = ""
        st.session_state.pdf_path = None
        st.session_state.pdf_result = None
        st.session_state.prepared_paper = None
        st.session_state.analysis_result = None
        st.session_state.analysis_error = None
        st.rerun()

    _render_paper_information(paper)
    _render_pdf_preview(pdf_path)

    if not st.session_state.analysis_running and st.session_state.analysis_result is None:
        if st.button("Run analysis again", type="primary"):
            _start_analysis(ServiceContainer(), pdf_path)


def _check_analysis_finished() -> None:
    """
    Transfer completed analysis from worker thread.
    """

    try:
        payload = _analysis_queue.get_nowait()

    except Empty:
        return

    st.session_state.analysis_running = False

    if isinstance(payload, dict) and not payload.get("ok", True):
        st.session_state.analysis_error = str(
            payload.get("error") or "Analysis failed."
        )
        st.session_state.analysis_result = None
        return

    result = payload.get("result") if isinstance(payload, dict) else payload
    st.session_state.analysis_result = result


# =============================================================================
# Page Information Rendering
# =============================================================================


def _render_paper_information(
    paper: PreparedPaper,
) -> None:
    """
    Render extracted paper information.
    """

    if paper is None:
        return

    st.subheader("📑 Paper Information")

    st.markdown("### Title")

    st.info(
        paper.title,
    )

    st.caption(f"Source: {paper.title_source}")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Pages",
            paper.total_pages,
        )

        st.metric(
            "Characters",
            f"{paper.total_characters:,}",
        )

    with col2:

        st.metric(
            "Title Confidence",
            f"{paper.title_confidence:.0%}",
        )

        st.metric(
            "Sections",
            paper.sections.section_count,
        )

    # st.markdown("### Title")

    # st.info(
    #     paper.title,
    # )

    # st.caption(
    #     f"Source: {paper.title_source}"
    # )

    available_sections = [
        field.name.replace("_", " ").title()
        for field in fields(paper.sections)
        if getattr(
            paper.sections,
            field.name,
        )
    ]

    if available_sections:

        st.markdown("### Detected Sections")

        st.write(", ".join(available_sections))


# =============================================================================
# PDF Preview
# =============================================================================


def _render_pdf_preview(
    pdf_path: Path,
) -> None:
    """
    Display complete PDF without browser toolbar.
    """

    st.subheader("Paper Preview")
    try:
        pdf_bytes = pdf_path.read_bytes()
    except OSError as exc:
        _LOGGER.warning("PDF preview unavailable: %s", exc)
        st.info("PDF preview is unavailable, but analysis can still continue.")
        return

    st.download_button(
        "Open or download uploaded PDF",
        data=pdf_bytes,
        file_name=pdf_path.name,
        mime="application/pdf",
        use_container_width=True,
    )
    st.caption(
        "Embedded PDF preview is disabled because Microsoft Edge can block "
        "local data-based PDF frames. This does not affect extraction or analysis."
    )


# =============================================================================
# Background Analysis
# =============================================================================


def _poll_analysis() -> None:
    """
    Poll background worker for completion on the Streamlit thread.
    """

    _check_analysis_finished()


def _start_analysis(
    container: ServiceContainer,
    pdf_path: Path,
) -> None:
    """
    Start analysis worker.
    """
    if pdf_path is None or st.session_state.prepared_paper is None:
        st.error("Please upload a valid research paper before starting analysis.")
        return

    progress_manager = ProgressManager()

    st.session_state.progress_manager = progress_manager

    st.session_state.analysis_result = None

    st.session_state.analysis_error = None

    st.session_state.analysis_running = True

    worker = threading.Thread(
        target=_analysis_worker,
        args=(
            container,
            pdf_path,
            progress_manager,
        ),
        daemon=True,
    )

    st.session_state.analysis_worker = worker

    worker.start()


def _analysis_worker(
    container: ServiceContainer,
    pdf_path: Path,
    progress_manager: ProgressManager,
) -> None:
    """
    Execute analysis in background.
    """

    try:
        request = AnalysisRequest(
            source_path=str(pdf_path),
            filename=pdf_path.name,
        )
        result = container.analysis_service.analyze(
            request,
            progress_reporter=progress_manager,
        )
        _analysis_queue.put({"ok": True, "result": result})

    except Exception as exc:
        _LOGGER.exception("Background analysis failed.")
        root_cause = exc
        while root_cause.__cause__ is not None:
            root_cause = root_cause.__cause__
        _analysis_queue.put(
            {
                "ok": False,
                "error": f"Analysis failed: {root_cause}",
            }
        )


# =============================================================================
# Progress Rendering
# =============================================================================


@st.fragment(run_every=1.0)
def _render_running_analysis() -> None:
    """
    Display live progress without rebuilding the complete Streamlit page.
    """

    was_running = st.session_state.analysis_running
    _check_analysis_finished()

    # Rebuild the complete page once so the final report replaces the live
    # progress fragment. During execution only this fragment is refreshed.
    if was_running and not st.session_state.analysis_running:
        st.rerun()

    # Show any errors
    if st.session_state.analysis_error:
        st.error(st.session_state.analysis_error)

    # If analysis is still running, show progress
    if st.session_state.analysis_running:
        progress_manager = st.session_state.progress_manager

        if progress_manager is not None:
            renderer = ProgressRenderer(progress_manager)
            renderer.render()

        return

    # Analysis completed successfully
    if st.session_state.analysis_result is not None:
        _render_result(st.session_state.analysis_result)


# =============================================================================
# Result Rendering
# =============================================================================


def _render_result(
    result: AnalysisResult,
) -> None:
    """
    Render final report.
    """

    st.divider()

    brand = get_brand_config()
    st.header(brand.document_title)

    content = result.analysis

    st.markdown(content)

    paper = st.session_state.get("prepared_paper")
    render_report_export(
        {
            "title": getattr(paper, "title", "Untitled Paper"),
            "filename": getattr(paper, "filename", "-"),
            "pages": getattr(paper, "total_pages", "-"),
            "characters": getattr(paper, "total_characters", "-"),
            "provider": result.provider,
            "model": result.model,
            "analysis": content,
            "research_gap": result.research_gap,
            "future_scope": result.future_scope,
        }
    )

    with st.expander("Analysis Information"):

        st.json(result.to_dict())


# =============================================================================
# File Utilities
# =============================================================================


def _save_uploaded_file(
    uploaded_file,
) -> Path:
    """
    Save uploaded PDF under the configured uploads directory.
    """

    upload_dir = get_application_config().paths.uploads_dir
    file_path = resolve_upload_path(upload_dir, uploaded_file.name)
    file_path.write_bytes(uploaded_file.getbuffer())
    return file_path
