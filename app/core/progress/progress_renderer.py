"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Renderer
File         : progress_renderer.py
Version      : 3.0.0

Description:
    Streamlit renderer for pipeline execution progress.

    Converts ProgressState into visual UI components.

===============================================================================
"""

from __future__ import annotations


from datetime import timedelta


import streamlit as st


from app.core.progress.progress_manager import (
    ProgressManager,
)


from app.core.progress.progress_state import (
    ProgressState,
)


__all__ = [
    "ProgressRenderer",
]



class ProgressRenderer:
    """
    Renders pipeline progress in Streamlit.

    This class contains only UI logic.
    """

    VERSION = "3.0.0"



    def __init__(
        self,
        progress_manager: ProgressManager,
    ) -> None:
        """
        Initialize renderer.

        Parameters
        ----------
        progress_manager:
            Runtime progress manager.
        """

        self._manager = progress_manager



    # ------------------------------------------------------------------
    # Public render API
    # ------------------------------------------------------------------

    def render(
        self,
    ) -> None:
        """
        Render current progress state.
        """

        state = self._manager.get_state()


        self._render_stage(
            state
        )


        self._render_progress_bar(
            state
        )


        self._render_message(
            state
        )


        self._render_elapsed_time(
            state
        )


        self._render_cancel_button()



    # ------------------------------------------------------------------
    # Components
    # ------------------------------------------------------------------

    def _render_stage(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render current pipeline stage.
        """

        if state.stage:

            st.subheader(
                 f"⚙️ {state.stage.name.replace('_', ' ').title()}"
            )



    def _render_progress_bar(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render percentage progress bar.
        """

        percentage = (
            state.percentage
            /
            100
        )


        st.progress(
            percentage
        )


        st.caption(
            f"{state.percentage:.0f}% completed"
        )



    def _render_message(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render progress message.
        """

        if state.status:

            st.info(
                state.status
            )



    def _render_elapsed_time(
        self,
        state: ProgressState,
    ) -> None:
        """
        Render elapsed execution time.
        """

        seconds = int(
            state.elapsed_seconds
        )


        elapsed = str(
            timedelta(
                seconds=seconds
            )
        )


        st.caption(
            f"Elapsed time: {elapsed}"
        )



    def _render_cancel_button(
        self,
    ) -> None:
        """
        Render cancellation control.
        """

        if st.button(
            "⛔ Stop Analysis",
        ):

            self._manager.cancel()


    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Renderer name.
        """

        return "Streamlit Progress Renderer"



    @property
    def version(
        self,
    ) -> str:
        """
        Renderer version.
        """

        return self.VERSION