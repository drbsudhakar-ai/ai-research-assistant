"""
AI Research Assistant
Pipeline Settings Package

Provides the complete Pipeline Settings module.

Public API:
    - PipelineSettings controller
    - PipelineSettingsState
    - Pipeline configuration enums

Architecture:

    Settings Page
          |
          ▼
    PipelineSettings
          |
          ├── Sections
          ├── Components
          └── State

Version:
    1.0.0
"""

from .pipeline_settings import (
    PipelineSettings,
)

from .state import (
    PipelineSettingsState,
)

from .enums import (
    PipelineExecutionMode,
    AnalysisMode,
    ProgressDisplayMode,
    RetryPolicy,
    PipelineStageType,
    LLMProcessingMode,
    CancellationMode,
    TimeoutPreset,
    ConcurrencyLevel,
)


__all__ = [

    # Controller

    "PipelineSettings",


    # State

    "PipelineSettingsState",


    # Enums

    "PipelineExecutionMode",

    "AnalysisMode",

    "ProgressDisplayMode",

    "RetryPolicy",

    "PipelineStageType",

    "LLMProcessingMode",

    "CancellationMode",

    "TimeoutPreset",

    "ConcurrencyLevel",
]