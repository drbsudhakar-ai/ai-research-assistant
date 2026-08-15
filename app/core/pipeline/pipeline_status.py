"""
===============================================================================
Project      : AI Research Assistant
Module       : Generic Pipeline Framework
File         : pipeline_status.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines the execution lifecycle states for a pipeline.

Responsibilities:
    - Represent the current execution state of a pipeline.
    - Provide a strongly typed alternative to string literals.
    - Improve readability and maintainability.

Non-Responsibilities:
    - Pipeline execution.
    - State transition validation.
===============================================================================
"""

from __future__ import annotations

from enum import Enum

__all__ = ["PipelineStatus"]


class PipelineStatus(Enum):
    """
    Represents the lifecycle state of a pipeline execution.
    """

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        """Return the string representation of the status."""
        return self.value