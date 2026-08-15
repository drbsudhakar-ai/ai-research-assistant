"""
===============================================================================
Project      : AI Research Assistant
Module       : Generic Pipeline Framework
File         : pipeline.py
Version      : 3.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines the immutable execution container for pipeline steps.

Responsibilities:
    - Store ordered pipeline steps.
    - Provide safe iteration.
    - Provide pipeline metadata.
    - Represent a configured workflow.

Non-Responsibilities:
    - Execute steps.
    - Manage progress.
    - Handle errors.
    - Perform business logic.

Design Notes:
    - Pipeline is intentionally lightweight.
    - Execution is delegated to PipelineRunner.
    - Steps are executed in registration order.
===============================================================================
"""

from __future__ import annotations

from collections.abc import (
    Iterator,
    Sequence,
)

from app.core.pipeline.base_pipeline_step import (
    BasePipelineStep,
)

__all__ = [
    "Pipeline",
]


class Pipeline:
    """
    Represents a configured pipeline.

    A Pipeline contains an ordered collection of pipeline steps.
    It does not execute them directly.

    Execution responsibility belongs to PipelineRunner.
    """

    def __init__(
        self,
        steps: Sequence[BasePipelineStep],
    ) -> None:
        """
        Initialize pipeline.

        Parameters
        ----------
        steps:
            Ordered collection of pipeline steps.

        Raises
        ------
        ValueError
            If steps are empty or invalid.
        """

        if steps is None:
            raise ValueError("Pipeline steps cannot be None.")

        if not steps:
            raise ValueError("Pipeline must contain at least one step.")

        for step in steps:
            if not isinstance(
                step,
                BasePipelineStep,
            ):
                raise TypeError(
                    "All pipeline steps must inherit " "from BasePipelineStep."
                )

        self._steps: tuple[BasePipelineStep, ...] = tuple(steps)

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def steps(
        self,
    ) -> tuple[BasePipelineStep, ...]:
        """
        Return configured pipeline steps.

        Returns
        -------
        tuple
            Immutable tuple of steps.
        """

        return self._steps

    @property
    def step_count(
        self,
    ) -> int:
        """
        Return number of pipeline steps.
        """

        return len(self._steps)

    @property
    def names(
        self,
    ) -> tuple[str, ...]:
        """
        Return pipeline step names.
        """

        return tuple(step.name for step in self._steps)

    # =========================================================================
    # Iteration Support
    # =========================================================================

    def __iter__(
        self,
    ) -> Iterator[BasePipelineStep]:
        """
        Iterate through pipeline steps.

        PipelineRunner uses this method during execution.
        """

        return iter(self._steps)

    def __len__(
        self,
    ) -> int:
        """
        Return number of configured steps.
        """

        return len(self._steps)

    # =========================================================================
    # Debug Representation
    # =========================================================================

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return f"{self.__class__.__name__}(" f"steps={self.names!r})"
