"""
===============================================================================
Project      : AI Research Assistant
Module       : Generic Pipeline Framework
File         : exceptions.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines the exception hierarchy for the generic pipeline framework.

Responsibilities:
    - Represent framework-specific runtime errors.
    - Support structured exception metadata.
    - Enable exception chaining.
    - Provide a stable exception model for all pipeline implementations.

Design Principles:
    - Lightweight
    - Immutable after construction
    - Framework agnostic
    - No business logic
===============================================================================
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "PipelineError",
    "PipelineConfigurationError",
    "PipelineExecutionError",
    "PipelineCancelledError",
    "PipelineContextError",
    "StepError",
    "StepValidationError",
    "StepExecutionError",
]


class PipelineError(RuntimeError):
    """
    Base class for all pipeline framework exceptions.
    """

    def __init__(
        self,
        message: str,
        *,
        step_name: str | None = None,
        step_type: type | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self._message = message
        self._step_name = step_name
        self._step_type = step_type
        self._cause = cause

    @property
    def message(self) -> str:
        return self._message

    @property
    def step_name(self) -> str | None:
        return self._step_name

    @property
    def step_type(self) -> type | None:
        return self._step_type

    @property
    def cause(self) -> Exception | None:
        return self._cause

    @property
    def step(self) -> str | None:
        """
        Human-readable step identifier.
        """
        if self._step_name:
            return self._step_name

        if self._step_type:
            return self._step_type.__name__

        return None

    def as_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "step_name": self.step_name,
            "step_type": (
                self.step_type.__name__
                if self.step_type is not None
                else None
            ),
            "cause": (
                type(self.cause).__name__
                if self.cause is not None
                else None
            ),
        }

    def __str__(self) -> str:
        parts = [self.message]

        if self.step:
            parts.append(f"Step: {self.step}")

        if self.cause:
            parts.append(f"Cause: {type(self.cause).__name__}")

        return "\n".join(parts)


class PipelineConfigurationError(PipelineError):
    """Raised when a pipeline is configured incorrectly."""


class PipelineExecutionError(PipelineError):
    """Raised when pipeline execution fails."""


class PipelineCancelledError(PipelineError):
    """Raised when pipeline execution is cancelled."""


class PipelineContextError(PipelineError):
    """Raised when the pipeline context is invalid."""


class StepError(PipelineError):
    """Base class for step-related exceptions."""


class StepValidationError(StepError):
    """Raised when a step receives invalid input."""


class StepExecutionError(StepError):
    """Raised when a step fails during execution."""

