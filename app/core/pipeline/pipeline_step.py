"""
Legacy compatibility alias for the canonical pipeline step ABC.

Canonical ABC (use in new code):
    app.core.pipeline.base_pipeline_step.BasePipelineStep

This name exists only so older imports of PipelineStep remain valid.
It is not a second contract.
"""

from __future__ import annotations

from app.core.pipeline.base_pipeline_step import BasePipelineStep

PipelineStep = BasePipelineStep

__all__ = [
    "PipelineStep",
]
