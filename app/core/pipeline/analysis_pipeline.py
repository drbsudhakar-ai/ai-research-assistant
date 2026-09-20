"""
Legacy compatibility name for ResearchAnalysisPipeline.

Canonical type:
    app.core.pipeline.research_analysis_pipeline.ResearchAnalysisPipeline

This module is not a second pipeline implementation.
"""

from __future__ import annotations

from app.core.pipeline.research_analysis_pipeline import (
    ResearchAnalysisPipeline,
)

AnalysisPipeline = ResearchAnalysisPipeline

__all__ = [
    "AnalysisPipeline",
]
