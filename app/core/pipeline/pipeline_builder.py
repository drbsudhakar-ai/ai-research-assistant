"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Pipeline
File         : pipeline_builder.py
Version      : 1.0.0

Description:
    Builder for constructing analysis pipelines.

Responsibilities:
    - Assemble pipeline steps.
    - Preserve execution order.
    - Validate pipeline configuration.
    - Create a PipelineRunner instance.
===============================================================================
"""

from __future__ import annotations

from app.core.pipeline.base_pipeline_step import BasePipelineStep
from app.core.pipeline.pipeline import Pipeline


class PipelineBuilder:
    """
    Builder for Pipeline.

    Steps must implement the canonical BasePipelineStep ABC.
    """

    def __init__(self) -> None:
        self._steps: list[BasePipelineStep] = []

    def add_step(
        self,
        step: BasePipelineStep,
    ) -> PipelineBuilder:
        """
        Add a pipeline step.
        """
        self._steps.append(step)
        return self

    def add_steps(
        self,
        steps: list[BasePipelineStep],
    ) -> PipelineBuilder:
        """
        Add multiple pipeline steps.
        """
        self._steps.extend(steps)
        return self

    def clear(self) -> PipelineBuilder:
        """
        Remove all configured steps.
        """
        self._steps.clear()
        return self

    @property
    def step_count(self) -> int:
        """
        Number of configured steps.
        """
        return len(self._steps)

    def build(self) -> Pipeline:
        """
        Create a configured Pipeline.

        Returns
        -------
        Pipeline
            Configured pipeline instance.
        """

        if not self._steps:
            raise ValueError("Pipeline contains no steps.")

        return Pipeline(list(self._steps))
