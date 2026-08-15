"""
===============================================================================
Project      : AI Research Assistant
File         : app_config.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
Application-wide configuration constants.

Identity values are sourced from BrandConfig.
===============================================================================
"""

from __future__ import annotations

from app.config.branding import get_brand_config

_BRAND = get_brand_config()

APP_NAME = _BRAND.application_name

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 1

APP_VERSION = _BRAND.version

APP_ICON = _BRAND.icon

PAGE_TITLE = _BRAND.page_title

DEVELOPER_MODE = False

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

AUTHOR = _BRAND.author

CREDIT = _BRAND.credit

COPYRIGHT = _BRAND.copyright

TAGLINE = _BRAND.tagline
