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



import base64
import time
import queue
import threading
from dataclasses import fields
from queue import Empty
from app.config.branding import get_brand_config
from app.models.prepared_paper import PreparedPaper

from pathlib import Path


import streamlit as st


from app.services.service_container import (
    ServiceContainer,
)

from app.core.progress.progress_manager import (
    ProgressManager,
)

from app.core.progress.progress_renderer import (
    ProgressRenderer,
)

from app.models.analysis_request import AnalysisRequest
from app.models.analysis_result import AnalysisResult
from app.ui.components.page import (
    render_page_header,
)
from app.ui.components.analyze.report_export import (
    render_report_export,
)

_analysis_queue = queue.Queue()


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

    _render_upload_section(
        container
    )

    _poll_analysis()

    _render_running_analysis()
    
    
def _auto_refresh() -> None:
    """
    Refresh the page while analysis is running.
    """

    if st.session_state.analysis_running:
        time.sleep(0.5)
        st.rerun()

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


    uploaded_file = st.file_uploader(

        "Upload Research Paper PDF",

        type=[
            "pdf"
        ],

        disabled=(
            st.session_state.analysis_running
        ),

    )
    if uploaded_file is None:
        st.session_state.pdf_path = None
        st.session_state.prepared_paper = None
        st.session_state.pdf_result = None
        st.info("Upload a research paper PDF to begin analysis.")
        return

    if uploaded_file:

        pdf_path = _save_uploaded_file(uploaded_file)

        st.session_state.pdf_path = pdf_path

        pdf_result = container.pdf_extractor.extract_text(
            uploaded_file
        )

        prepared_paper = container.paper_preprocessor.prepare(
            extracted=pdf_result,
            filename=uploaded_file.name,
        )

        st.session_state.prepared_paper = prepared_paper

        st.session_state.pdf_result = pdf_result

        st.success(uploaded_file.name)

        _render_paper_information(
            prepared_paper
        )

        _render_pdf_preview(
            pdf_path
        )


    if not st.session_state.analysis_running:

        if st.button(

            "🚀 Analyze Paper",

            type="primary",

            disabled=(

                st.session_state.analysis_running
                or st.session_state.prepared_paper is None

            ),

        ):

            _start_analysis(
                container,
                st.session_state.pdf_path,
            )

def _check_analysis_finished() -> None:
    """
    Transfer completed analysis from worker thread.
    """

    try:
        result = _analysis_queue.get_nowait()

    except Empty:
        return

    st.session_state.analysis_result = result

    st.session_state.analysis_running = False

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

    st.caption(
            f"Source: {paper.title_source}"
        )


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

        st.markdown(
            "### Detected Sections"
        )

        st.write(
            ", ".join(
                available_sections
            )
        )

# =============================================================================
# PDF Preview
# =============================================================================


def _render_pdf_preview(
    pdf_path: Path,
) -> None:
    """
    Display complete PDF without browser toolbar.
    """


    encoded = base64.b64encode(

        pdf_path.read_bytes()

    ).decode(
        "utf-8"
    )


    html = f"""

    <iframe

        src="data:application/pdf;base64,{encoded}"

        width="100%"

        height="800px"

        style="border:none;">

    </iframe>

    """


    st.subheader(
        "Paper Preview"
    )


    st.iframe(
        html,
        height=920
    )
    # st.components.v1.html(

    #     html,

    #     height=820,

    # )



# =============================================================================
# Background Analysis
# =============================================================================

def _poll_analysis() -> None:
    """
    Poll background worker for completion.
    """

    if not st.session_state.analysis_running:
        return

    try:
        result = _analysis_queue.get_nowait()

    except queue.Empty:
        return

    st.session_state.analysis_running = False

    st.session_state.analysis_result = result

    if getattr(result, "error", None):
        st.session_state.analysis_error = str(result.error)
        
        
def _start_analysis(
    container: ServiceContainer,
    pdf_path: Path,
) -> None:
    """
    Start analysis worker.
    """
    if (
        pdf_path is None
        or st.session_state.prepared_paper is None
    ):
        st.error(
            "Please upload a valid research paper before starting analysis."
        )
        return

    progress_manager = ProgressManager()


    st.session_state.progress_manager = (
        progress_manager
    )


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
        _analysis_queue.put(result)

    except Exception:
        st.session_state.analysis_error = (
            "Analysis failed. Please retry with a valid paper."
        )

    finally:
        st.session_state.analysis_running = False



# =============================================================================
# Progress Rendering
# =============================================================================

def _render_running_analysis() -> None:
    """
    Display live analysis progress.
    """

    # First update worker status
    _check_analysis_finished()

    # Show any errors
    if st.session_state.analysis_error:
        st.error(st.session_state.analysis_error)

    # If analysis is still running, show progress
    if st.session_state.analysis_running:
        progress_manager = st.session_state.progress_manager

        if progress_manager is not None:
            renderer = ProgressRenderer(progress_manager)
            renderer.render()

        # Refresh only while running
        _auto_refresh()

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
    st.header(
        brand.document_title
    )


    content = result.analysis


    st.markdown(
        content
    )

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
        }
    )


    with st.expander(
        "Analysis Information"
    ):

        st.json(
            result.to_dict()
        )



# =============================================================================
# File Utilities
# =============================================================================


def _save_uploaded_file(
    uploaded_file,
) -> Path:
    """
    Save uploaded PDF.
    """


    upload_dir = Path(
        "data/uploads"
    )


    upload_dir.mkdir(

        parents=True,

        exist_ok=True,

    )


    file_path = (

        upload_dir

        /

        uploaded_file.name

    )


    file_path.write_bytes(

        uploaded_file.getbuffer()

    )


    return file_path