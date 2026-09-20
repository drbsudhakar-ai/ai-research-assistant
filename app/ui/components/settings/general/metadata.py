"""
AI Research Assistant
General Settings - Metadata Definitions

Provides UI metadata for General Settings options.

This module contains:
    - Display labels
    - Descriptions
    - Help text
    - UI grouping information

No Streamlit dependency.
No state handling.
No business logic.

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass

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
# Metadata Model
# ============================================================

@dataclass(frozen=True)
class SettingMetadata:
    """
    Common metadata structure for settings options.
    """

    label: str
    description: str
    help_text: str
    icon: str | None = None


# ============================================================
# Theme Metadata
# ============================================================

THEME_METADATA: dict[ThemeMode, SettingMetadata] = {
    ThemeMode.SYSTEM: SettingMetadata(
        label="System Default",
        description="Automatically follow operating system theme.",
        help_text="Uses your device light/dark preference.",
        icon="🖥️",
    ),
    ThemeMode.LIGHT: SettingMetadata(
        label="Light Theme",
        description="Use a bright application interface.",
        help_text="Recommended for well-lit environments.",
        icon="☀️",
    ),
    ThemeMode.DARK: SettingMetadata(
        label="Dark Theme",
        description="Use a dark application interface.",
        help_text="Reduces eye strain in low-light environments.",
        icon="🌙",
    ),
}


# ============================================================
# UI Density Metadata
# ============================================================

UI_DENSITY_METADATA: dict[UIDensity, SettingMetadata] = {
    UIDensity.COMPACT: SettingMetadata(
        label="Compact",
        description="Displays more information with reduced spacing.",
        help_text="Suitable for smaller screens and power users.",
        icon="📐",
    ),
    UIDensity.COMFORTABLE: SettingMetadata(
        label="Comfortable",
        description="Balanced spacing and readability.",
        help_text="Recommended default layout.",
        icon="⚖️",
    ),
    UIDensity.SPACIOUS: SettingMetadata(
        label="Spacious",
        description="Uses larger spacing for improved readability.",
        help_text="Suitable for presentations and accessibility.",
        icon="🖼️",
    ),
}


# ============================================================
# Language Metadata
# ============================================================

LANGUAGE_METADATA: dict[ApplicationLanguage, SettingMetadata] = {
    ApplicationLanguage.ENGLISH: SettingMetadata(
        label="English",
        description="Application language.",
        help_text="Default application language.",
        icon="🌐",
    ),
}


# ============================================================
# Startup Page Metadata
# ============================================================

STARTUP_PAGE_METADATA: dict[StartupPage, SettingMetadata] = {
    StartupPage.HOME: SettingMetadata(
        label="Home Dashboard",
        description="Open the dashboard when application starts.",
        help_text="Recommended for general usage.",
        icon="🏠",
    ),
    StartupPage.ANALYZE: SettingMetadata(
        label="Analyze Paper",
        description="Open directly to paper analysis.",
        help_text="Useful for research workflows.",
        icon="📄",
    ),
    StartupPage.HISTORY: SettingMetadata(
        label="Analysis History",
        description="Open previous analysis records.",
        help_text="Useful for reviewing previous work.",
        icon="📚",
    ),
}


# ============================================================
# Auto Save Metadata
# ============================================================

AUTO_SAVE_METADATA: dict[AutoSaveMode, SettingMetadata] = {
    AutoSaveMode.ENABLED: SettingMetadata(
        label="Enabled",
        description="Automatically save completed analyses.",
        help_text="Recommended to prevent data loss.",
        icon="💾",
    ),
    AutoSaveMode.DISABLED: SettingMetadata(
        label="Disabled",
        description="Disable automatic saving.",
        help_text="Results must be saved manually.",
        icon="⏸️",
    ),
}


# ============================================================
# History Storage Metadata
# ============================================================

HISTORY_STORAGE_METADATA: dict[HistoryStorageMode, SettingMetadata] = {
    HistoryStorageMode.LOCAL_DATABASE: SettingMetadata(
        label="Local Database",
        description="Store history inside application database.",
        help_text="Default SQLite storage.",
        icon="🗄️",
    ),
    HistoryStorageMode.CUSTOM_PATH: SettingMetadata(
        label="Custom Location",
        description="Store history in a user-selected location.",
        help_text="Useful for backups and external storage.",
        icon="📁",
    ),
}


# ============================================================
# Confirmation Metadata
# ============================================================

CONFIRMATION_METADATA: dict[ConfirmationMode, SettingMetadata] = {
    ConfirmationMode.ALWAYS: SettingMetadata(
        label="Always Confirm",
        description="Ask before every important action.",
        help_text="Provides maximum safety.",
        icon="🔒",
    ),
    ConfirmationMode.DESTRUCTIVE_ONLY: SettingMetadata(
        label="Destructive Actions Only",
        description="Confirm only irreversible actions.",
        help_text="Recommended workflow.",
        icon="⚠️",
    ),
    ConfirmationMode.NEVER: SettingMetadata(
        label="Never Confirm",
        description="Skip confirmation prompts.",
        help_text="For experienced users.",
        icon="⚡",
    ),
}


# ============================================================
# Date Format Metadata
# ============================================================

DATE_FORMAT_METADATA: dict[DateFormat, SettingMetadata] = {
    DateFormat.ISO: SettingMetadata(
        label="ISO Format (YYYY-MM-DD)",
        description="International date format.",
        help_text="Recommended for technical applications.",
        icon="📅",
    ),
    DateFormat.LOCAL: SettingMetadata(
        label="Local Format (DD-MM-YYYY)",
        description="Day-first date format.",
        help_text="Common regional format.",
        icon="📅",
    ),
    DateFormat.US: SettingMetadata(
        label="US Format (MM-DD-YYYY)",
        description="Month-first date format.",
        help_text="Common US format.",
        icon="📅",
    ),
}


# ============================================================
# Logging Metadata
# ============================================================

LOGGING_LEVEL_METADATA: dict[LoggingLevel, SettingMetadata] = {
    LoggingLevel.DEBUG: SettingMetadata(
        label="Debug",
        description="Detailed diagnostic information.",
        help_text="Useful during development.",
        icon="🐞",
    ),
    LoggingLevel.INFO: SettingMetadata(
        label="Info",
        description="Standard application information.",
        help_text="Recommended default.",
        icon="ℹ️",
    ),
    LoggingLevel.WARNING: SettingMetadata(
        label="Warning",
        description="Only warnings and errors.",
        help_text="Reduces log volume.",
        icon="⚠️",
    ),
    LoggingLevel.ERROR: SettingMetadata(
        label="Error",
        description="Only critical failures.",
        help_text="Minimal logging output.",
        icon="❌",
    ),
}


# ============================================================
# Export
# ============================================================

__all__ = [
    "SettingMetadata",
    "THEME_METADATA",
    "UI_DENSITY_METADATA",
    "LANGUAGE_METADATA",
    "STARTUP_PAGE_METADATA",
    "AUTO_SAVE_METADATA",
    "HISTORY_STORAGE_METADATA",
    "CONFIRMATION_METADATA",
    "DATE_FORMAT_METADATA",
    "LOGGING_LEVEL_METADATA",
]