"""
===============================================================================
Project      : AI Research Assistant
Module       : Research Analysis Pipeline
File         : research_analysis_pipeline.py
Version      : 1.0.0

Description:
    Production research paper analysis pipeline.

    Responsible for composing the complete paper analysis workflow by
    registering pipeline steps in execution order.

Pipeline Flow:

    Validate PDF
          |
          v
    Prepare Paper
          |
          v
    Analyze Paper
          |
          v
    Save History
          |
          v
    Generate Result

===============================================================================
"""

from __future__ import annotations

from collections.abc import Sequence

from app.core.pipeline.base_pipeline_step import BasePipelineStep
from app.core.pipeline.pipeline import Pipeline

__all__ = [
    "ResearchAnalysisPipeline",
]


class ResearchAnalysisPipeline(Pipeline):
    """
    Pipeline implementation for research paper analysis.

    This class only composes workflow steps.
    Business logic belongs inside individual pipeline steps.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        steps: Sequence[BasePipelineStep] | None = None,
    ) -> None:
        """
        Initialize research analysis pipeline.

        Parameters
        ----------
        steps:
            Optional custom pipeline steps.

            If not provided, default production
            research analysis workflow is created.
        """

        if steps is None:
            raise TypeError(
                "ResearchAnalysisPipeline requires configured steps. "
                "Use ResearchAnalysisPipelineFactory.create()."
            )

        super().__init__(
            steps=steps,
        )

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Pipeline display name.
        """

        return "Research Paper Analysis Pipeline"

    @property
    def version(
        self,
    ) -> str:
        """
        Pipeline version.
        """

        return self.VERSION
