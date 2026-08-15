"""
===============================================================================
Project      : AI Research Assistant
File         : ui_config.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
User interface configuration.
===============================================================================
"""

from __future__ import annotations

from app.config.branding import get_brand_config

# =============================================================================
# Sidebar
# =============================================================================

SIDEBAR_TITLE = "Navigation"

SHOW_APP_VERSION = True

SHOW_AUTHOR = True

SHOW_COPYRIGHT = True

# =============================================================================
# Dashboard
# =============================================================================

WELCOME_TITLE = f"Welcome to {get_brand_config().application_name}"

WELCOME_MESSAGE = get_brand_config().tagline

# =============================================================================
# Messages
# =============================================================================

LOADING_MESSAGE = "Analyzing paper..."

SUCCESS_MESSAGE = "Analysis completed successfully."

ERROR_MESSAGE = "An unexpected error occurred."
