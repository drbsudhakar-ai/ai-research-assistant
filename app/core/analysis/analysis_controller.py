"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Lifecycle Controller
File         : analysis_controller.py
Version      : 4.0.0
Author       : Dr. B. Sudhakar

Description:
    Production controller for research paper analysis execution.

Responsibilities:
    - Own analysis lifecycle.
    - Start background execution.
    - Update AnalysisState.
    - Connect Pipeline with ProgressManager.
    - Handle failures.
    - Support cancellation.
    - Provide Streamlit-safe monitoring.

Architecture:

    UI
     |
     v
    AnalysisController
     |
     +--> AnalysisState
     |
     +--> Worker Thread
     |
     +--> Analysis Pipeline
     |
     +--> ProgressManager

===============================================================================
"""

from __future__ import annotations


from datetime import datetime
from threading import Thread
from typing import Any
import traceback

from app.core.progress.progress_manager import ProgressManager
from app.core.analysis.analysis_state import (
    AnalysisState,
)

from app.core.analysis.analysis_status import (
    AnalysisStatus,
)

from app.core.analysis.progress_bridge import (
    ProgressBridge,
)

class AnalysisController:
    """
    Controls one complete analysis execution.

    The controller is the only component allowed
    to mutate AnalysisState during execution.
    """


    def __init__(
        self,
        state: AnalysisState,
        pipeline: Any,
        progress_manager=None,
    ) -> None:


        self.state = state

        self.pipeline = pipeline
        self.progress_manager = progress_manager

        self.progress_bridge = (
            ProgressBridge(state)
        )
        self.progress_reporter = ProgressManager()

        # self.progress_reporter = ProgressManager(
        #     self._progress_callback
        # )


    # ==================================================================
    # START ANALYSIS
    # ==================================================================

    def start(
        self,
    ) -> None:
        """
        Start analysis in background thread.
        """


        if self.state.is_running:

            return


        self.state.start()



        worker = Thread(

            target=self._execute,

            daemon=True,

            name="analysis-worker",

        )


        self.state.worker = worker


        worker.start()



    # ==================================================================
    # WORKER EXECUTION
    # ==================================================================

    def _execute(
        self,
    ) -> None:
        """
        Background execution entry point.
        """


        try:

            self.state.message = (
                "Starting analysis pipeline..."
            )


            result = self.pipeline.execute(
                self.state.prepared_paper,
                progress_reporter=self.progress_reporter,

            )


            if self.state.cancelled:

                return



            self.state.complete(

                result,

            )



        except Exception as ex:


            traceback.print_exc()


            self.state.fail(

                ex,

            )



    # ==================================================================
    # MONITOR
    # ==================================================================

    def monitor(
        self,
    ) -> AnalysisState:
        """
        Called repeatedly by Streamlit reruns.

        Does not block.
        """


        worker = self.state.worker


        if worker is None:

            return self.state



        if worker.is_alive():

            return self.state



        #
        # Worker finished
        #

        if self.state.status == AnalysisStatus.RUNNING:


            self.state.fail(

                RuntimeError(
                    "Worker stopped unexpectedly"
                )

            )


        return self.state



    # ==================================================================
    # CANCEL
    # ==================================================================

    def cancel(
        self,
    ) -> None:
        """
        Request cancellation.
        """


        if not self.state.is_running:

            return


        self.state.cancel()



    # ==================================================================
    # RESULT
    # ==================================================================

    def get_result(
        self,
    ) -> Any | None:
        """
        Return completed analysis result.
        """


        if self.state.has_result:

            return self.state.analysis_result


        return None



    # ==================================================================
    # ERROR
    # ==================================================================

    def get_error(
        self,
    ) -> str | None:
        """
        Return execution error.
        """


        if self.state.has_error:

            return self.state.error_message


        return None

    def _progress_callback(
        self,
        percentage,
        stage,
        message,
    ):
        """
        Receives progress from pipeline.
        """

        self.progress_bridge.update(

            percentage,

            stage,

            message,

        )

    # ==================================================================
    # STATUS
    # ==================================================================

    @property
    def is_running(
        self,
    ) -> bool:

        return self.state.is_running



    @property
    def is_completed(
        self,
    ) -> bool:

        return self.state.is_completed



    @property
    def is_failed(
        self,
    ) -> bool:

        return self.state.is_failed