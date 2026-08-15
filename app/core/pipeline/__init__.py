"""
Canonical pipeline package.

Canonical ABC (final contract):
    BasePipelineStep

Legacy compatibility alias (same type, not a second ABC):
    PipelineStep

PipelineStage is a stage-name enum, not a step ABC.

ResearchAnalysisPipelineFactory is imported by the composition root,
not re-exported here, to avoid pulling PDF/LLM infrastructure into
core pipeline imports.
"""

from app.core.pipeline.base_pipeline_step import BasePipelineStep
from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.pipeline_builder import PipelineBuilder
from app.core.pipeline.pipeline_context import PipelineContext
from app.core.pipeline.pipeline_result import PipelineResult
from app.core.pipeline.pipeline_runner import PipelineRunner
from app.core.pipeline.pipeline_stage import PipelineStage
from app.core.pipeline.pipeline_step import PipelineStep
from app.core.pipeline.research_analysis_pipeline import (
    ResearchAnalysisPipeline,
)

__all__ = [
    "BasePipelineStep",
    "Pipeline",
    "PipelineBuilder",
    "PipelineContext",
    "PipelineResult",
    "PipelineRunner",
    "PipelineStage",
    "PipelineStep",
    "ResearchAnalysisPipeline",
]
