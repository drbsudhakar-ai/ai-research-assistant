"""
AI Research Assistant
General Settings - Validators

Provides validation rules for General Settings configuration.

This module validates:
    - Application preferences
    - Storage paths
    - UI configuration
    - Runtime preferences

No Streamlit dependency.
No UI rendering.
No state management.

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
# Generic Helpers
# ============================================================


def validate_enum_value(
    value: object,
    enum_type: type,
) -> tuple[bool, str]:
    """
    Validate that a value belongs to an enum.

    Returns:
        (is_valid, message)
    """

    if isinstance(value, enum_type):
        return True, ""

    return (
        False,
        f"Invalid value '{value}'. "
        f"Expected {enum_type.__name__}.",
    )


# ============================================================
# Application Settings Validation
# ============================================================


def validate_app_name(
    app_name: str,
) -> tuple[bool, str]:
    """
    Validate application name.
    """

    if not app_name:
        return False, "Application name cannot be empty."

    if len(app_name.strip()) < 3:
        return (
            False,
            "Application name must contain at least 3 characters.",
        )

    return True, ""


# ============================================================
# UI Settings Validation
# ============================================================


def validate_theme_mode(
    value: ThemeMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        ThemeMode,
    )


def validate_ui_density(
    value: UIDensity,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        UIDensity,
    )


def validate_language(
    value: ApplicationLanguage,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        ApplicationLanguage,
    )


# ============================================================
# Startup Validation
# ============================================================


def validate_startup_page(
    value: StartupPage,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        StartupPage,
    )


# ============================================================
# Storage Validation
# ============================================================


def validate_workspace_path(
    path: Path | str,
) -> tuple[bool, str]:
    """
    Validate workspace directory.
    """

    try:
        workspace = Path(path)

    except Exception:
        return False, "Invalid workspace path."

    if not workspace.exists():
        return (
            False,
            "Workspace directory does not exist.",
        )

    if not workspace.is_dir():
        return (
            False,
            "Workspace path must be a directory.",
        )

    return True, ""


def validate_history_path(
    path: Path | str,
) -> tuple[bool, str]:
    """
    Validate history database path.
    """

    try:
        history_path = Path(path)

    except Exception:
        return False, "Invalid history path."

    if history_path.suffix != ".db":
        return (
            False,
            "History storage file must be a SQLite database (.db).",
        )

    parent = history_path.parent

    if not parent.exists():
        return (
            False,
            "History directory does not exist.",
        )

    return True, ""


def validate_history_storage_mode(
    value: HistoryStorageMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        HistoryStorageMode,
    )


# ============================================================
# Behaviour Validation
# ============================================================


def validate_auto_save_mode(
    value: AutoSaveMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        AutoSaveMode,
    )


def validate_confirmation_mode(
    value: ConfirmationMode,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        ConfirmationMode,
    )


# ============================================================
# Date / Logging Validation
# ============================================================


def validate_date_format(
    value: DateFormat,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        DateFormat,
    )


def validate_logging_level(
    value: LoggingLevel,
) -> tuple[bool, str]:

    return validate_enum_value(
        value,
        LoggingLevel,
    )


# ============================================================
# Complete Configuration Validation
# ============================================================


def validate_general_settings(
    settings: dict,
) -> tuple[bool, list[str]]:
    """
    Validate complete General Settings configuration.

    Returns:
        (
            is_valid,
            list_of_errors
        )
    """

    errors: list[str] = []

    validators = [
        (
            "app_name",
            validate_app_name,
        ),
        (
            "theme_mode",
            validate_theme_mode,
        ),
        (
            "ui_density",
            validate_ui_density,
        ),
        (
            "language",
            validate_language,
        ),
        (
            "startup_page",
            validate_startup_page,
        ),
        (
            "history_storage_mode",
            validate_history_storage_mode,
        ),
        (
            "auto_save_mode",
            validate_auto_save_mode,
        ),
        (
            "confirmation_mode",
            validate_confirmation_mode,
        ),
        (
            "date_format",
            validate_date_format,
        ),
        (
            "logging_level",
            validate_logging_level,
        ),
    ]

    for key, validator in validators:

        if key not in settings:
            continue

        valid, message = validator(
            settings[key]
        )

        if not valid:
            errors.append(
                f"{key}: {message}"
            )

    if "workspace_path" in settings:

        valid, message = validate_workspace_path(
            settings["workspace_path"]
        )

        if not valid:
            errors.append(
                f"workspace_path: {message}"
            )

    if "history_path" in settings:

        valid, message = validate_history_path(
            settings["history_path"]
        )

        if not valid:
            errors.append(
                f"history_path: {message}"
            )

    return (
        len(errors) == 0,
        errors,
    )


# ============================================================
# Export
# ============================================================

__all__ = [
    "validate_enum_value",
    "validate_app_name",
    "validate_theme_mode",
    "validate_ui_density",
    "validate_language",
    "validate_startup_page",
    "validate_workspace_path",
    "validate_history_path",
    "validate_history_storage_mode",
    "validate_auto_save_mode",
    "validate_confirmation_mode",
    "validate_date_format",
    "validate_logging_level",
    "validate_general_settings",
]