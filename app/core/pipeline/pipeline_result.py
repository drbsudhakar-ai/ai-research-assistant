"""
===============================================================================
Project      : AI Research Assistant
Module       : Generic Pipeline Framework
File         : pipeline_result.py
Version      : 3.0.0
Author       : Dr. B. Sudhakar

Description:
    Represents the output of a pipeline execution.

Responsibilities:
    - Store execution success/failure state.
    - Store pipeline context.
    - Store execution duration.
    - Store produced result.
    - Store failure diagnostics.

Non-Responsibilities:
    - Execute pipeline steps.
    - Handle UI rendering.
    - Perform business logic.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.pipeline.pipeline_context import PipelineContext


__all__ = [
    "PipelineResult",
]


@dataclass(slots=True)
class PipelineResult:
    """
    Result produced after pipeline execution.

    A pipeline always returns this object after execution.
    """

    success: bool

    context: PipelineContext

    execution_time: float

    result: Any | None = None

    error: Exception | None = None

    failed_step: str | None = None


    # =========================================================================
    # Factory Methods
    # =========================================================================

    @classmethod
    def success_result(
        cls,
        *,
        context: PipelineContext,
        execution_time: float,
        result: Any | None = None,
    ) -> "PipelineResult":
        """
        Create successful pipeline result.
        """

        return cls(
            success=True,
            context=context,
            execution_time=execution_time,
            result=result,
            error=None,
            failed_step=None,
        )


    @classmethod
    def failure_result(
        cls,
        *,
        context: PipelineContext,
        error: Exception,
        failed_step: str | None,
        execution_time: float,
    ) -> "PipelineResult":
        """
        Create failed pipeline result.
        """

        return cls(
            success=False,
            context=context,
            execution_time=execution_time,
            result=None,
            error=error,
            failed_step=failed_step,
        )


    # =========================================================================
    # Convenience Properties
    # =========================================================================

    @property
    def failed(
        self,
    ) -> bool:
        """
        Return True when pipeline failed.
        """

        return not self.success


    @property
    def has_result(
        self,
    ) -> bool:
        """
        Return True when execution produced output.
        """

        return self.result is not None


    @property
    def error_message(
        self,
    ) -> str | None:
        """
        Return readable error message.
        """

        if self.error is None:
            return None

        return str(self.error)


    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"success={self.success}, "
            f"execution_time={self.execution_time:.2f}, "
            f"failed_step={self.failed_step!r}"
            ")"
        )