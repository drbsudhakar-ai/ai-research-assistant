"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Background Worker
File         : analyze_worker.py

Description:
    Executes research paper analysis in a background thread.

Responsibilities:
    - Run AnalysisService pipeline
    - Update analysis state
    - Handle failures
    - Preserve Streamlit rerun compatibility

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import Any

import streamlit as st


from app.ui.pages.analyze_v5_draft.analyze_state import (
    ANALYSIS_ERROR_KEY,
    ANALYSIS_RESULT_KEY,
    ANALYSIS_RUNNING_KEY,
    ANALYSIS_COMPLETED_KEY,
    mark_analysis_completed,
    mark_analysis_failed,
)


# =============================================================================
# Worker Function
# =============================================================================


def analysis_worker(
    container: Any,
    pdf_path: Path,
    progress_manager: Any | None = None,
) -> None:
    """
    Execute paper analysis pipeline.

    This function is designed to run inside a background thread.

    Args:
        container:
            Application service container.

        pdf_path:
            PDF file path.

        progress_manager:
            Optional progress manager instance.
    """

    print(
        ">>> Analysis worker started"
    )

    try:

        # ---------------------------------------------------------
        # Initial Progress
        # ---------------------------------------------------------

        if progress_manager:

            progress_manager.update(
                stage="Starting analysis",
                progress=0.05,
                message="Initializing pipeline",
            )


        # ---------------------------------------------------------
        # Execute Analysis Service
        # ---------------------------------------------------------

        print(
            ">>> Calling AnalysisService.analyze()"
        )


        result = (
            container.analysis_service.analyze(

                pdf_path=pdf_path,

                metadata={
                    "source": "streamlit",
                },

                progress_manager=progress_manager,

            )
        )


        print(
            ">>> Analysis completed successfully"
        )


        # ---------------------------------------------------------
        # Final Progress
        # ---------------------------------------------------------

        if progress_manager:

            progress_manager.update(

                stage="Completed",

                progress=1.0,

                message="Analysis completed",

            )


        # ---------------------------------------------------------
        # Store Result
        # ---------------------------------------------------------

        st.session_state[
            ANALYSIS_RESULT_KEY
        ] = result


        st.session_state[
            ANALYSIS_RUNNING_KEY
        ] = False


        st.session_state[
            ANALYSIS_COMPLETED_KEY
        ] = True


        st.session_state[
            ANALYSIS_ERROR_KEY
        ] = None



    except Exception as exc:

        print(
            "!!! Analysis worker failed"
        )

        traceback.print_exc()


        # ---------------------------------------------------------
        # Progress Error
        # ---------------------------------------------------------

        if progress_manager:

            try:

                progress_manager.update(

                    stage="Failed",

                    progress=1.0,

                    message=str(exc),

                )

            except Exception:

                pass



        # ---------------------------------------------------------
        # Store Failure
        # ---------------------------------------------------------

        mark_analysis_failed(
            exc
        )


    finally:

        print(
            ">>> Analysis worker finished"
        )
