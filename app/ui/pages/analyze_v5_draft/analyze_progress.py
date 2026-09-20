"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Progress UI
File         : analyze_progress.py

Description:
    Streamlit progress rendering component for paper analysis.

Responsibilities:
    - Bind Streamlit containers
    - Display analysis progress
    - Display current pipeline stage
    - Display status messages

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Any

import streamlit as st


# =============================================================================
# Progress Renderer
# =============================================================================


class AnalyzeProgressRenderer:
    """
    Handles progress display for Analyze page.
    """

    def __init__(self) -> None:

        self.placeholder = None


    # -------------------------------------------------------------------------
    # Binding
    # -------------------------------------------------------------------------

    def bind(
        self,
        placeholder: Any,
    ) -> None:
        """
        Bind Streamlit placeholder.

        Args:
            placeholder:
                st.empty() container.
        """

        self.placeholder = placeholder



    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    def render(
        self,
        progress_manager: Any | None,
    ) -> None:
        """
        Render current progress.

        Args:
            progress_manager:
                Active ProgressManager instance.
        """

        if self.placeholder is None:

            return


        if progress_manager is None:

            return



        try:

            state = (
                progress_manager.get_state()
            )


        except Exception:

            return



        if state is None:

            return



        progress = (
            getattr(
                state,
                "progress",
                0.0,
            )
        )


        stage = (
            getattr(
                state,
                "stage",
                "Processing",
            )
        )


        message = (
            getattr(
                state,
                "message",
                "",
            )
        )



        percentage = int(
            progress * 100
        )



        with self.placeholder.container():

            st.markdown(
                f"""
                ### 🔬 Analysis Progress

                **Stage:** {stage}

                {message}

                **{percentage}% completed**
                """
            )


            st.progress(
                progress
            )



    # -------------------------------------------------------------------------
    # Clear
    # -------------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove progress display.
        """

        if self.placeholder:

            self.placeholder.empty()



# =============================================================================
# Helper Factory
# =============================================================================


def create_progress_renderer() -> AnalyzeProgressRenderer:
    """
    Create progress renderer instance.
    """

    return AnalyzeProgressRenderer()