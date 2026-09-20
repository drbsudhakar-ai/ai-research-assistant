"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Session Manager
File         : analysis_session_manager.py
Version      : 4.0.0
Author       : Dr. B. Sudhakar

Description:
    Streamlit session lifecycle manager for analysis execution.

Responsibilities:
    - Persist AnalysisState.
    - Persist AnalysisController.
    - Restore execution after reruns.
    - Prevent duplicate analysis workers.
    - Provide a single access point for UI.

Design:
    Streamlit session_state contains only runtime references.

===============================================================================
"""

from __future__ import annotations


import streamlit as st


from app.core.analysis.analysis_state import (
    AnalysisState,
)

from app.core.analysis.analysis_controller import (
    AnalysisController,
)



class AnalysisSessionManager:
    """
    Manages analysis runtime objects inside Streamlit session.

    This class hides Streamlit session_state implementation details.
    """



    STATE_KEY = (
        "analysis_state"
    )

    CONTROLLER_KEY = (
        "analysis_controller"
    )



    # ==================================================================
    # INITIALIZATION
    # ==================================================================

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize required session objects.
        """


        if cls.STATE_KEY not in st.session_state:

            st.session_state[
                cls.STATE_KEY
            ] = AnalysisState()



        if cls.CONTROLLER_KEY not in st.session_state:

            st.session_state[
                cls.CONTROLLER_KEY
            ] = None



    # ==================================================================
    # STATE ACCESS
    # ==================================================================

    @classmethod
    def get_state(
        cls,
    ) -> AnalysisState:
        """
        Return current analysis state.
        """


        cls.initialize()


        return st.session_state[
            cls.STATE_KEY
        ]



    # ==================================================================
    # CONTROLLER ACCESS
    # ==================================================================

    @classmethod
    def get_controller(
        cls,
    ) -> AnalysisController | None:
        """
        Return active controller.
        """


        cls.initialize()


        return st.session_state[
            cls.CONTROLLER_KEY
        ]



    @classmethod
    def set_controller(
        cls,
        controller: AnalysisController,
    ) -> None:
        """
        Store controller.
        """


        st.session_state[
            cls.CONTROLLER_KEY
        ] = controller



    # ==================================================================
    # LIFECYCLE CHECKS
    # ==================================================================

    @classmethod
    def is_running(
        cls,
    ) -> bool:
        """
        Check whether analysis is active.
        """


        state = cls.get_state()


        return state.is_running



    @classmethod
    def has_result(
        cls,
    ) -> bool:
        """
        Check completed result.
        """


        state = cls.get_state()


        return state.has_result



    @classmethod
    def has_error(
        cls,
    ) -> bool:
        """
        Check failed analysis.
        """


        state = cls.get_state()


        return state.has_error



    # ==================================================================
    # START PROTECTION
    # ==================================================================

    @classmethod
    def can_start(
        cls,
    ) -> bool:
        """
        Prevent duplicate workers.

        Returns:
            True if new analysis can start.
        """


        state = cls.get_state()


        if state.is_running:

            return False


        return True



    # ==================================================================
    # RESET
    # ==================================================================

    @classmethod
    def reset(
        cls,
    ) -> None:
        """
        Clear current analysis lifecycle.
        """


        state = cls.get_state()


        state.reset()


        st.session_state[
            cls.CONTROLLER_KEY
        ] = None



    # ==================================================================
    # CANCEL
    # ==================================================================

    @classmethod
    def cancel(
        cls,
    ) -> None:
        """
        Cancel running analysis.
        """


        controller = (
            cls.get_controller()
        )


        if controller:

            controller.cancel()