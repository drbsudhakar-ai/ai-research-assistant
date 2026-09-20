"""
===============================================================================
Project      : AI Research Assistant
Module       : Progress Bridge
File         : progress_bridge.py
Version      : 5.0.0
Author       : Dr. B. Sudhakar

Description:
    Connects pipeline progress events with AnalysisState.

===============================================================================
"""


from __future__ import annotations



from app.core.analysis.analysis_state import (
    AnalysisState,
)



class ProgressBridge:
    """
    Adapter between ProgressManager and AnalysisState.
    """



    def __init__(
        self,
        state: AnalysisState,
    ):

        self.state = state



    def update(
        self,
        percentage: int,
        stage: str,
        message: str,
    ) -> None:
        """
        Update runtime analysis state.
        """


        self.state.progress = percentage

        self.state.progress_state.stage = stage

        self.state.progress_state.message = message

        self.state.message = message