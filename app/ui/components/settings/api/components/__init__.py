"""
app/ui/components/settings/api/components/__init__.py

Reusable API Settings UI component exports.

Components:
- Provider cards
- Status badges
- API key input
- Model selector
- Settings metrics
- Save actions

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations


# ============================================================================
# Provider Components
# ============================================================================

from .provider_card import (
    render_provider_card,
    render_provider_grid,
)


# ============================================================================
# Status Components
# ============================================================================

from .status_badge import (
    StatusType,
    render_status_badge,
    render_connected_badge,
    render_error_badge,
    render_pending_badge,
    render_disabled_badge,
)


# ============================================================================
# Credential Components
# ============================================================================

from .api_key_input import (
    render_api_key_input,
    mask_key,
)


# ============================================================================
# Model Components
# ============================================================================

from .model_selector import (
    render_model_selector,
    render_model_summary,
)


# ============================================================================
# Metric Components
# ============================================================================

from .settings_metric import (
    render_settings_metric,
    render_provider_metrics,
    render_connection_metrics,
    render_generation_metrics,
    render_configuration_status,
)


# ============================================================================
# Action Components
# ============================================================================

from .save_actions import (
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

    # Provider
    "render_provider_card",
    "render_provider_grid",


    # Status
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