"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Service
File         : analysis_service.py
Version      : 4.0.0
Author       : Dr. B. Sudhakar

Description:
    Application service responsible for managing paper analysis workflow.

Responsibilities:
    - Create analysis lifecycle.
    - Coordinate controller.
    - Provide UI-safe API.
    - Hide pipeline implementation details.
    - Manage analysis state.

Architecture:

    Streamlit
        |
        v
    AnalysisService
        |
        v
    AnalysisController
        |
        v
    ResearchAnalysisPipeline

===============================================================================
"""


from __future__ import annotations


from typing import Any


from app.core.analysis.analysis_state import (
    AnalysisState,
)

from app.core.analysis.analysis_controller import (
    AnalysisController,
)



class AnalysisService:
    """
    High-level application service.

    This is the only class UI components should call.
    """


    def __init__(
        self,
        pipeline,
        progress_manager=None,
    ) -> None:
        """
        Args:
            pipeline_factory:
                Callable responsible for creating
                analysis pipeline instances.
        """

        self.pipeline = pipeline
        self.progress_manager = progress_manager


    # ==================================================================
    # CREATE STATE
    # ==================================================================

    def create_state(
        self,
    ) -> AnalysisState:
        """
        Create fresh lifecycle state.
        """

        return AnalysisState()



    # ==================================================================
    # START
    # ==================================================================

    def start_analysis(
        self,
        state: AnalysisState,
        paper: Any,
    ) -> AnalysisController:
        """
        Start new analysis execution.

        Args:
            state:
                Current AnalysisState.

            paper:
                Prepared paper object.
        """


        #
        # Store paper
        #

        state.prepared_paper = paper



        #
        # Create pipeline
        #

        pipeline = self.pipeline




        #
        # Create controller
        #

        controller = AnalysisController(

            state=state,

            pipeline=pipeline,

            progress_manager=self.progress_manager,

        )


        #
        # Start worker
        #

        controller.start()


        return controller



    # ==================================================================
    # MONITOR
    # ==================================================================

    def monitor(
        self,
        controller: AnalysisController,
    ) -> AnalysisState:
        """
        Monitor running analysis.

        Called on every Streamlit rerun.
        """

        return controller.monitor()



    # ==================================================================
    # CANCEL
    # ==================================================================

    def cancel(
        self,
        controller: AnalysisController,
    ) -> None:
        """
        Cancel running analysis.
        """

        controller.cancel()



    # ==================================================================
    # RESULT
    # ==================================================================

    def get_result(
        self,
        state: AnalysisState,
    ) -> Any | None:
        """
        Return final analysis result.
        """

        return state.analysis_result



    # ==================================================================
    # STATUS
    # ==================================================================

    def is_running(
        self,
        state: AnalysisState,
    ) -> bool:
        """
        Check execution state.
        """

        return state.is_running



    def is_completed(
        self,
        state: AnalysisState,
    ) -> bool:

        return state.is_completed



    def has_error(
        self,
        state: AnalysisState,
    ) -> bool:

        return state.has_error