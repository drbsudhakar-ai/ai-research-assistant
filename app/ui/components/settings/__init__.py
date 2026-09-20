"""
app/ui/components/settings/__init__.py

Settings UI Components Package

Provides reusable Streamlit components for
AI Research Assistant application settings.

Version:
    1.0.0

Author:
    Dr B Sudhakar

Components:
    - General Settings
    - LLM Settings
    - Provider Settings
    - Export Settings
    - About Settings
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# General Settings
# ---------------------------------------------------------------------------

from app.ui.components.settings.general_settings import (
    render_general_settings,
)


# ---------------------------------------------------------------------------
# LLM Settings
# ---------------------------------------------------------------------------

from app.ui.components.settings.llm_settings import (
    render_llm_settings,
)


# ---------------------------------------------------------------------------
# Provider Settings
# ---------------------------------------------------------------------------

from app.ui.components.settings.provider_settings import (
    render_provider_settings,
)


# ---------------------------------------------------------------------------
# Export Settings
# ---------------------------------------------------------------------------

from app.ui.components.settings.export_settings import (
    render_export_settings,
)


# ---------------------------------------------------------------------------
# About Settings
# ---------------------------------------------------------------------------

from app.ui.components.settings.about_settings import (
    render_about_settings,
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "render_general_settings",
    "render_llm_settings",
    "render_provider_settings",
    "render_export_settings",
    "render_about_settings",
]