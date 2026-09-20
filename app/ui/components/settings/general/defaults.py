"""
AI Research Assistant
General Settings - Default Values

Defines default configuration values for the General Settings module.

This module contains:
    - Application preferences
    - Default UI behaviour
    - Default storage preferences
    - Default user experience settings

No Streamlit dependency.
No state handling.
No business logic.

Version:
    1.0.0
"""

from __future__ import annotations

from pathlib import Path

from .enums import (
    ThemeMode,
    UIDensity,
    ApplicationLanguage,
    StartupPage,
    AutoSaveMode,
    HistoryStorageMode,
    ConfirmationMode,
    DateFormat,
    LoggingLevel,
)


# ============================================================
# Application Defaults
# ============================================================

DEFAULT_APP_NAME: str = "AI Research Assistant"


# ============================================================
# UI Defaults
# ============================================================

DEFAULT_THEME_MODE: ThemeMode = ThemeMode.SYSTEM

DEFAULT_UI_DENSITY: UIDensity = UIDensity.COMFORTABLE

DEFAULT_LANGUAGE: ApplicationLanguage = (
    ApplicationLanguage.ENGLISH
)


# ============================================================
# Startup Behaviour Defaults
# ============================================================

DEFAULT_STARTUP_PAGE: StartupPage = StartupPage.HOME


# ============================================================
# Storage Defaults
# ============================================================

DEFAULT_WORKSPACE_PATH: Path = Path.cwd()

DEFAULT_HISTORY_STORAGE_MODE: HistoryStorageMode = (
    HistoryStorageMode.LOCAL_DATABASE
)


DEFAULT_HISTORY_PATH: Path = (
    DEFAULT_WORKSPACE_PATH / "data" / "history.db"
)


# ============================================================
# Auto Save Defaults
# ============================================================

DEFAULT_AUTO_SAVE_MODE: AutoSaveMode = (
    AutoSaveMode.ENABLED
)


# ============================================================
# Confirmation Defaults
# ============================================================

DEFAULT_CONFIRMATION_MODE: ConfirmationMode = (
    ConfirmationMode.DESTRUCTIVE_ONLY
)


# ============================================================
# Date / Time Defaults
# ============================================================

DEFAULT_DATE_FORMAT: DateFormat = DateFormat.ISO


# ============================================================
# Logging Defaults
# ============================================================

DEFAULT_LOGGING_LEVEL: LoggingLevel = (
    LoggingLevel.INFO
)


# ============================================================
# UI Behaviour Flags
# ============================================================

DEFAULT_SHOW_TOOLTIPS: bool = True

DEFAULT_SHOW_ADVANCED_OPTIONS: bool = False

DEFAULT_ENABLE_ANIMATIONS: bool = True


# ============================================================
# Security / Privacy Defaults
# ============================================================

DEFAULT_REMEMBER_LAST_PAGE: bool = True

DEFAULT_CLEAR_TEMP_FILES_ON_EXIT: bool = False


# ============================================================
# Performance Defaults
# ============================================================

DEFAULT_CACHE_ENABLED: bool = True


# ============================================================
# Exported Symbols
# ============================================================

__all__ = [
    "DEFAULT_APP_NAME",
    "DEFAULT_THEME_MODE",
    "DEFAULT_UI_DENSITY",
    "DEFAULT_LANGUAGE",
    "DEFAULT_STARTUP_PAGE",
    "DEFAULT_WORKSPACE_PATH",
    "DEFAULT_HISTORY_STORAGE_MODE",
    "DEFAULT_HISTORY_PATH",
    "DEFAULT_AUTO_SAVE_MODE",
    "DEFAULT_CONFIRMATION_MODE",
    "DEFAULT_DATE_FORMAT",
    "DEFAULT_LOGGING_LEVEL",
    "DEFAULT_SHOW_TOOLTIPS",
    "DEFAULT_SHOW_ADVANCED_OPTIONS",
    "DEFAULT_ENABLE_ANIMATIONS",
    "DEFAULT_REMEMBER_LAST_PAGE",
    "DEFAULT_CLEAR_TEMP_FILES_ON_EXIT",
    "DEFAULT_CACHE_ENABLED",
]