"""
===============================================================================
Project      : AI Research Assistant
File         : app_config.py
Version      : 1.2.0
Author       : Dr. B. Sudhakar

Description:
Compatibility constants for application-wide identity and layout.

Identity values are sourced from BrandConfig.
Runtime developer mode is sourced from ApplicationConfig. Prefer
``get_application_config()`` for new code.
===============================================================================
"""

from __future__ import annotations

from app.config.branding import get_brand_config
from app.config.loader import get_application_config

_BRAND = get_brand_config()

APP_NAME = _BRAND.application_name

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 1

APP_VERSION = _BRAND.version

APP_ICON = _BRAND.icon

PAGE_TITLE = _BRAND.page_title

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

AUTHOR = _BRAND.author

CREDIT = _BRAND.credit

COPYRIGHT = _BRAND.copyright

TAGLINE = _BRAND.tagline


def is_developer_mode() -> bool:
    """Return the live developer-mode flag from ApplicationConfig."""

    return get_application_config().application.developer_mode


def __getattr__(name: str) -> object:
    if name == "DEVELOPER_MODE":
        return is_developer_mode()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
