"""
===============================================================================
Project      : AI Research Assistant
Module       : Generic Pipeline Framework
File         : base_pipeline_step.py
Version      : 3.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines the abstract base class for all pipeline execution steps.

Responsibilities:
    - Provide common pipeline step contract.
    - Validate execution context.
    - Control step execution lifecycle.
    - Provide step identification.

Non-Responsibilities:
    - Business logic.
    - Progress rendering.
    - Error recovery.
    - Pipeline orchestration.

Design Notes:
    - This is the canonical (final) pipeline step ABC.
    - PipelineStep is a compatibility alias of this class, not a second ABC.
    - All concrete pipeline steps must inherit from this class.
    - PipelineRunner calls run().
    - Subclasses implement execute().
===============================================================================
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import Generic, TypeVar

from app.core.pipeline.pipeline_context import (
    PipelineContext,
)

__all__ = [
    "BasePipelineStep",
]


T = TypeVar("T")


class BasePipelineStep(
    ABC,
    Generic[T],
):
    """
    Abstract base class for pipeline steps.

    Each step performs one isolated unit of workflow logic.
    """

    # =========================================================================
    # Step Identity
    # =========================================================================

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Return human-readable step name.

        Example:
            "Validate PDF"
        """
        ...

    # =========================================================================
    # Execution Entry Point
    # =========================================================================

    def run(
        self,
        context: PipelineContext[T],
    ) -> None:
        """
        Execute this pipeline step.

        This method is called by PipelineRunner.

        Parameters
        ----------
        context:
            Shared pipeline execution context.

        Raises
        ------
        ValueError
            If context is invalid.
        """

        if context is None:
            raise ValueError("Pipeline context cannot be None.")

        self.execute(context)

    # =========================================================================
    # Business Implementation
    # =========================================================================

    @abstractmethod
    def execute(
        self,
        context: PipelineContext[T],
    ) -> None:
        """
        Execute step-specific business logic.

        Concrete pipeline steps implement this method.

        Parameters
        ----------
        context:
            Shared pipeline context.
        """
        ...

    # =========================================================================
    # Debug Support
    # =========================================================================

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return f"{self.__class__.__name__}(" f"name={self.name!r}" ")"
