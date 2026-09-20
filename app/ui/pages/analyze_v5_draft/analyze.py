"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Paper Page Controller
File         : analyze.py

Description:
    Main Streamlit controller for research paper analysis workflow.

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations


import threading
import time
from pathlib import Path


import streamlit as st

from app.services.service_container import ServiceContainer
# from app.container import ServiceContainer


from app.ui.pages.analyze_v5_draft.analyze_state import (
    initialize_state,
    is_analysis_running,
    mark_analysis_started,
    PDF_PATH_KEY,
    PREPARED_PAPER_KEY,
    PDF_RESULT_KEY,
    PROGRESS_MANAGER_KEY,
    WORKER_THREAD_KEY,
)


from app.ui.pages.analyze_v5_draft.analyze_worker import (
    analysis_worker,
)


from app.ui.pages.analyze_v5_draft.analyze_preview import (
    save_uploaded_pdf,
    render_pdf_preview,
)


from app.ui.pages.analyze_v5_draft.analyze_info import (
    render_paper_information,
)


from app.ui.pages.analyze_v5_draft.analyze_report import (
    render_analysis_report,
)


from app.ui.pages.analyze_v5_draft.analyze_progress import (
    create_progress_renderer,
)



# =============================================================================
# Main Render
# =============================================================================


def render() -> None:
    """
    Render Analyze Paper page.
    """

    initialize_state()


    st.title(
        "📄 Analyze Research Paper"
    )


    container = ServiceContainer()



    _render_upload_section(
        container
    )


    _render_existing_content()


    _refresh_progress()



# =============================================================================
# Upload Section
# =============================================================================


def _render_upload_section(
    container: ServiceContainer,
) -> None:
    """
    Render PDF uploader and analysis button.
    """

    uploaded_file = st.file_uploader(

        "Upload Research Paper (PDF)",

        type=["pdf"],

        disabled=is_analysis_running(),

    )


    if uploaded_file is None:

        return



    if (
        PDF_PATH_KEY not in st.session_state
        or
        st.session_state[PDF_PATH_KEY] is None
    ):


        upload_dir = Path(
            "data/uploads"
        )


        pdf_path = save_uploaded_pdf(

            uploaded_file,

            upload_dir / uploaded_file.name,

        )


        st.session_state[
            PDF_PATH_KEY
        ] = pdf_path



        pdf_path = st.session_state[
            PDF_PATH_KEY
        ]


        st.success(
            f"Loaded: {pdf_path.name}"
        )


        _prepare_paper_information(
            container=container,
            pdf_path=pdf_path,
            filename=uploaded_file.name,
        )


        render_pdf_preview(
            pdf_path
        )



    if st.button(

        "🚀 Start Analysis",

        disabled=is_analysis_running(),

        type="primary",

    ):


        _start_analysis(
            container,
            pdf_path,
        )

        st.rerun()



# =============================================================================
# Start Worker
# =============================================================================


def _start_analysis(
    container: ServiceContainer,
    pdf_path: Path,
) -> None:
    """
    Start background analysis worker.
    """


    if is_analysis_running():

        return



    mark_analysis_started()



    # ---------------------------------------------------------
    # Progress Manager
    # ---------------------------------------------------------

    progress_manager = (
        container.progress_manager
        if hasattr(
            container,
            "progress_manager",
        )
        else None
    )


    st.session_state[
        PROGRESS_MANAGER_KEY
    ] = progress_manager



    # ---------------------------------------------------------
    # Progress Renderer
    # ---------------------------------------------------------

    if (
        "analysis_progress_renderer"
        not in st.session_state
    ):

        st.session_state[
            "analysis_progress_renderer"
        ] = create_progress_renderer()



    # ---------------------------------------------------------
    # Worker Thread
    # ---------------------------------------------------------

    worker = threading.Thread(

        target=analysis_worker,

        args=(

            container,

            pdf_path,

            progress_manager,

        ),

        daemon=True,

    )


    st.session_state[
        WORKER_THREAD_KEY
    ] = worker


    worker.start()



# =============================================================================
# Existing State Rendering
# =============================================================================


def _render_existing_content() -> None:
    """
    Render prepared paper information and report.
    """


    prepared_paper = st.session_state.get(
        PREPARED_PAPER_KEY
    )


    if prepared_paper:

        render_paper_information(
            prepared_paper
        )



    analysis_result = st.session_state.get(
        "analysis_result"
    )


    if analysis_result:

        render_analysis_report(
            analysis_result
        )



# =============================================================================
# Progress Refresh
# =============================================================================


def _refresh_progress() -> None:
    """
    Refresh progress UI while worker runs.
    """


    if not is_analysis_running():

        return



    placeholder = st.empty()



    renderer = st.session_state.get(
        "analysis_progress_renderer"
    )


    if renderer:

        renderer.bind(
            placeholder
        )


        renderer.render(

            st.session_state.get(
                PROGRESS_MANAGER_KEY
            )

        )



    # allow reruns while worker executes

    time.sleep(
        1
    )


    st.rerun()

def _prepare_paper_information(
    container: ServiceContainer,
    pdf_path: Path,
    filename: str,
) -> None:
    """
    Prepare paper metadata immediately after upload.
    """

    if st.session_state.get(
        PREPARED_PAPER_KEY
    ):
        return

    try:

        with open(
            pdf_path,
            "rb",
        ) as pdf_file:

            extraction_result = (
                container.pdf_extractor.extract_text(
                    pdf_file
                )
            )


        prepared_paper = (
            container.paper_preprocessor.prepare(
                extracted=extraction_result,
                filename=filename,
            )
        )


        st.session_state[
            PREPARED_PAPER_KEY
        ] = prepared_paper


    except Exception as exc:

        st.warning(
            f"Paper information extraction failed: {exc}"
        )
