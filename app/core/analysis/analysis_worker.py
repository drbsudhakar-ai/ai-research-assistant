"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Lifecycle
File         : analysis_worker.py
Version      : 5.0.0
Author       : Dr. B. Sudhakar

Description:
    Background execution worker for research paper analysis.

Responsibilities:
    - Execute AnalysisService.
    - Execute on a background thread.
    - Never modify AnalysisState.
    - Never access Streamlit.
    - Never render UI.
    - Never manage lifecycle.

Lifecycle ownership belongs exclusively to AnalysisController.

===============================================================================
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass
from typing import Any

from app.core.progress.progress_reporter import ProgressReporter
from app.models.analysis_request import AnalysisRequest
from app.services.analysis_service import AnalysisService


# =============================================================================
# Worker Result
# =============================================================================


@dataclass(slots=True)
class WorkerResult:
    """
    Result produced by AnalysisWorker.

    The controller is responsible for interpreting this object and
    updating AnalysisState.
    """

    success: bool

    result: Any | None = None

    error: Exception | None = None


# =============================================================================
# Worker
# =============================================================================


class AnalysisWorker:
    """
    Executes the analysis pipeline.

    This class intentionally knows nothing about:

        • Streamlit
        • Session State
        • AnalysisState
        • UI
        • Controller
    """

    def __init__(
        self,
        analysis_service: AnalysisService,
    ) -> None:

        self._analysis_service = analysis_service

    def run(
        self,
        *,
        request: AnalysisRequest,
        progress_reporter: ProgressReporter | None = None,
    ) -> WorkerResult:
        """
        Execute analysis.

        Parameters
        ----------
        request:
            Analysis request.

        progress_reporter:
            Progress callback.

        Returns
        -------
        WorkerResult
        """

        try:

            result = self._analysis_service.analyze(
                request=request,
                progress_reporter=progress_reporter,
            )

            return WorkerResult(
                success=True,
                result=result,
            )

        except Exception as ex:

            traceback.print_exc()

            return WorkerResult(
                success=False,
                error=ex,
            )