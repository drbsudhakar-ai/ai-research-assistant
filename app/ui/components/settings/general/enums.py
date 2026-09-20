"""
AI Research Assistant
General Settings - Enumerations

Defines controlled values used by the General Settings module.

This module contains only enums.
No UI logic.
No Streamlit dependencies.
No state management.

Version:
    1.0.0
"""

from __future__ import annotations

from enum import Enum


# ============================================================
# Theme Settings
# ============================================================

class ThemeMode(str, Enum):
    """
    Application theme modes.
    """

    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


# ============================================================
# UI Density Settings
# ============================================================

class UIDensity(str, Enum):
    """
    Controls application UI spacing density.
    """

    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    SPACIOUS = "spacious"


# ============================================================
# Language Settings
# ============================================================

class ApplicationLanguage(str, Enum):
    """
    Supported application languages.

    Future versions can extend this enum
    when internationalization is introduced.
    """

    ENGLISH = "en"


# ============================================================
# Startup Behaviour
# ============================================================

class StartupPage(str, Enum):
    """
    Default page opened when application starts.
    """

    HOME = "home"
    ANALYZE = "analyze"
    HISTORY = "history"


# ============================================================
# Auto Save Behaviour
# ============================================================

class AutoSaveMode(str, Enum):
    """
    Controls automatic saving behaviour.
    """

    ENABLED = "enabled"
    DISABLED = "disabled"


# ============================================================
# History Storage Settings
# ============================================================

class HistoryStorageMode(str, Enum):
    """
    Defines how analysis history is stored.
    """

    LOCAL_DATABASE = "local_database"
    CUSTOM_PATH = "custom_path"


# ============================================================
# Confirmation Behaviour
# ============================================================

class ConfirmationMode(str, Enum):
    """
    Controls confirmation prompts.
    """

    ALWAYS = "always"
    DESTRUCTIVE_ONLY = "destructive_only"
    NEVER = "never"


# ============================================================
# Date / Time Display
# ============================================================

class DateFormat(str, Enum):
    """
    Supported date display formats.
    """

    ISO = "yyyy-mm-dd"
    LOCAL = "dd-mm-yyyy"
    US = "mm-dd-yyyy"


# ============================================================
# Logging Preferences
# ============================================================

class LoggingLevel(str, Enum):
    """
    Application logging verbosity.
    """

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# ============================================================
# Exported Symbols
# ============================================================

__all__ = [
    "ThemeMode",
    "UIDensity",
    "ApplicationLanguage",
    "StartupPage",
    "AutoSaveMode",
    "HistoryStorageMode",
    "ConfirmationMode",
    "DateFormat",
    "LoggingLevel",
]