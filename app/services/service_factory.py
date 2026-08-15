"""
Legacy compatibility factory.

Canonical composition root:
    app.services.service_container.ServiceContainer

This class must not construct a parallel pipeline or service graph.
"""

from __future__ import annotations

from app.services.analysis_service import AnalysisService
from app.services.service_container import ServiceContainer

__all__ = ["ServiceFactory"]


class ServiceFactory:
    """Delegates to ServiceContainer."""

    @classmethod
    def create_analysis_service(cls) -> AnalysisService:
        return ServiceContainer().analysis_service
