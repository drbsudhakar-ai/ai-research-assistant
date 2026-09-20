"""
app/ui/components/settings/api/__init__.py

API Settings UI package.

Provides:
- Main API settings page
- Modular settings sections
- Reusable UI components
- API settings state integration

Architecture:

    api/
    |
    ├── api_settings.py
    ├── sections/
    ├── components/
    └── state/

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations


# ============================================================================
# Main Controller
# ============================================================================

from .api_settings import (
    render_api_settings,
)



# ============================================================================
# Sections
# ============================================================================

from .sections import (
    render_provider_section,
    render_connection_section,
    render_model_section,
    render_generation_section,
    render_advanced_section,
    render_connection_test,
)



# ============================================================================
# Components
# ============================================================================

from .components import (

    # Provider
    render_provider_card,
    render_provider_grid,


    # Status
    StatusType,
    render_status_badge,
    render_connected_badge,
    render_error_badge,
    render_pending_badge,
    render_disabled_badge,


    # Credentials
    render_api_key_input,
    mask_key,


    # Model
    render_model_selector,
    render_model_summary,


    # Metrics
    render_settings_metric,
    render_provider_metrics,
    render_connection_metrics,
    render_generation_metrics,
    render_configuration_status,


    # Actions
    render_save_actions,
    render_change_indicator,
)



# ============================================================================
# Package Metadata
# ============================================================================

__version__ = "1.0.0"



# ============================================================================
# Public API
# ============================================================================

__all__ = [

    # Main
    "render_api_settings",


    # Sections
    "render_provider_section",
    "render_connection_section",
    "render_model_section",
    "render_generation_section",
    "render_advanced_section",
    "render_connection_test",


    # Provider Components
    "render_provider_card",
    "render_provider_grid",


    # Status Components
    "StatusType",
    "render_status_badge",
    "render_connected_badge",
    "render_error_badge",
    "render_pending_badge",
    "render_disabled_badge",


    # API Key
    "render_api_key_input",
    "mask_key",


    # Model
    "render_model_selector",
    "render_model_summary",


    # Metrics
    "render_settings_metric",
    "render_provider_metrics",
    "render_connection_metrics",
    "render_generation_metrics",
    "render_configuration_status",


    # Actions
    "render_save_actions",
    "render_change_indicator",


    # Version
    "__version__",
]