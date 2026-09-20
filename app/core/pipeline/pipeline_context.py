"""
===============================================================================
Project      : AI Research Assistant
Module       : Pipeline Context
File         : pipeline_context.py
Version      : 2.0.0

Description:
    Shared execution context passed between pipeline steps.

    Stores workflow data, runtime services, progress reporting,
    and cancellation support.

===============================================================================
"""

from __future__ import annotations

from app.core.progress.progress_stage import ProgressStage
from dataclasses import dataclass, field
from typing import Any


from app.core.progress.progress_reporter import (
    ProgressReporter,
)

from app.core.progress.cancellation_token import (
    CancellationToken,
)


__all__ = [
    "PipelineContext",
]



@dataclass(slots=True)
class PipelineContext:
    """
    Runtime context shared across pipeline execution.

    Pipeline steps communicate only through this object.
    """


    # ------------------------------------------------------------------
    # Pipeline data
    # ------------------------------------------------------------------

    data: dict[str, Any] = field(
        default_factory=dict
    )


    # ------------------------------------------------------------------
    # Runtime services
    # ------------------------------------------------------------------

    progress_reporter: ProgressReporter | None = None


    cancellation_token: CancellationToken | None = None



    # ------------------------------------------------------------------
    # Execution metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # ------------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store pipeline data.
        """

        self.data[key] = value



    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve pipeline data.
        """

        return self.data.get(
            key,
            default,
        )



    def update(
        self,
        values: dict[str, Any],
    ) -> None:
        """
        Update multiple values.
        """

        self.data.update(
            values
        )



    # ------------------------------------------------------------------
    # Progress helpers
    # ------------------------------------------------------------------

    def report_progress(
        self,
        message: str,
        percentage: float | None = None,
        stage: ProgressStage | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Send progress update if reporter exists.
        """

        if self.progress_reporter is None:

            return


        self.progress_reporter.update(

            message=message,

            percentage=percentage,

            stage=stage,

            metadata=metadata,

        )



    # ------------------------------------------------------------------
    # Cancellation helpers
    # ------------------------------------------------------------------

    def is_cancelled(
        self,
    ) -> bool:
        """
        Check whether execution was cancelled.
        """

        if self.cancellation_token is None:

            return False


        return self.cancellation_token.is_cancelled()



    def raise_if_cancelled(
        self,
    ) -> None:
        """
        Stop execution if cancellation requested.
        """

        if self.is_cancelled():

            raise RuntimeError(
                "Pipeline execution cancelled"
            )