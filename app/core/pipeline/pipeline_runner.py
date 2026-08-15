"""
===============================================================================
Project      : AI Research Assistant
Module       : Pipeline Runner
File         : pipeline_runner.py
Version      : 1.0.0

Description:
    Executes pipeline workflows.

    PipelineRunner is responsible for lifecycle management of pipeline
    execution while keeping individual pipeline steps independent.

Execution Flow:

    Pipeline
        |
        v
    PipelineRunner
        |
        +--> Step 1
        |
        +--> Step 2
        |
        +--> Step 3
        |
        +--> Step N
        |
        v
    PipelineResult

===============================================================================
"""

from __future__ import annotations

from time import perf_counter
from traceback import format_exc

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.pipeline_context import PipelineContext
from app.core.pipeline.pipeline_result import PipelineResult


__all__ = [
    "PipelineRunner",
]


class PipelineRunner:
    """
    Executes pipeline workflows.

    The runner contains no business logic.
    It only controls execution lifecycle.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        pipeline: Pipeline,
    ) -> None:
        """
        Initialize pipeline runner.

        Parameters
        ----------
        pipeline:
            Pipeline instance to execute.
        """

        self._pipeline = pipeline


    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> PipelineResult:
        """
        Execute pipeline.

        Parameters
        ----------
        context:
            Shared pipeline execution context.

        Returns
        -------
        PipelineResult
            Final execution result.
        """

        start_time = perf_counter()
        
        step=None
        
        
        try:
            print(">>> PipelineRunner.run() started")
            for step in self._pipeline.steps:

                #
                # Cancellation support
                #
                if self._is_cancelled(context):
                    return PipelineResult.failure_result(
                        context=context,
                        error=RuntimeError("Pipeline execution cancelled"),
                        failed_step=None,
                        execution_time=perf_counter() - start_time,
                    )

                #
                # Execute current step
                #
                step.execute(
                    context,
                )


                #
                # Progress update
                #
                self._update_progress(
                    context,
                    step.name,
                )


            execution_time = (
                perf_counter() - start_time
            )


            return PipelineResult.success_result(
                context=context,
                execution_time=execution_time,
                result=context.data,
            )


        except Exception as exc:

            return PipelineResult.failure_result(
                context=context,
                error=exc,
                failed_step=(step, "name", None),
                execution_time=perf_counter() - start_time,
            )


    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_cancelled(
        self,
        context: PipelineContext,
    ) -> bool:
        """
        Check cancellation request.
        """

        token = getattr(
            context,
            "cancellation_token",
            None,
        )

        if token is None:
            return False

        return token.is_cancelled()


    def _update_progress(
        self,
        context: PipelineContext,
        step_name: str,
    ) -> None:
        """
        Notify progress listeners.

        Kept optional because pipeline execution
        should work without UI.
        """

        reporter = getattr(
            context,
            "progress_reporter",
            None,
        )

        if reporter is None:
            return


        reporter.update(
            message=f"Completed: {step_name}",
        )


    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Runner name.
        """

        return "Pipeline Runner"


    @property
    def version(
        self,
    ) -> str:
        """
        Runner version.
        """

        return self.VERSION