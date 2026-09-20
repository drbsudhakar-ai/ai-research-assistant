"""
AI Research Assistant
Pipeline Settings Sections Package

Contains UI sections for Pipeline Settings.

Sections:
    - Analysis configuration
    - Processing behaviour
    - Performance tuning

Version:
    1.0.0
"""

from .analysis_section import (
    AnalysisSection,
)

from .processing_section import (
    ProcessingSection,
)

from .performance_section import (
    PerformanceSection,
)


__all__ = [
    "AnalysisSection",
    "ProcessingSection",
    "PerformanceSection",
]