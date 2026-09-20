"""
Legacy compatibility bootstrap.

Canonical composition root:
    app.services.service_container.ServiceContainer
"""

from __future__ import annotations

from app.services.analysis_service import AnalysisService
from app.services.service_container import ServiceContainer

__all__ = ["build_analysis_service"]


def build_analysis_service() -> AnalysisService:
    return ServiceContainer().analysis_service
