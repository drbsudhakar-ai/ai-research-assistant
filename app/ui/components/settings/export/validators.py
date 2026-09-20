"""
Export Settings UI Validators

Contains validation logic for export configuration
before saving or applying settings.

Responsibilities:
- Validate export configuration values
- Provide user-friendly validation messages
- Prevent invalid export settings

Does NOT contain:
- Export generation logic
- File writing operations
- Streamlit rendering code
- Persistence handling

Version:
    1.0.0
"""

from __future__ import annotations

import re
from pathlib import Path

from app.ui.components.settings.export.enums import (
    ExportFormat,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_FILENAME_PATTERN_LENGTH = 120

VALID_FILENAME_VARIABLES = {
    "{title}",
    "{timestamp}",
}


# ---------------------------------------------------------------------------
# Individual Validators
# ---------------------------------------------------------------------------


def validate_export_format(
    export_format: ExportFormat | str,
) -> tuple[bool, str]:
    """
    Validate selected export format.

    Args:
        export_format:
            Selected export format.

    Returns:
        Tuple:
            (is_valid, message)
    """

    if isinstance(export_format, str):
        try:
            export_format = ExportFormat(export_format)
        except ValueError:
            return (
                False,
                "Unsupported export format selected.",
            )

    if not isinstance(export_format, ExportFormat):
        return (
            False,
            "Invalid export format configuration.",
        )

    return True, "Valid export format."


def validate_output_directory(
    output_directory: str,
) -> tuple[bool, str]:
    """
    Validate export output directory.

    Note:
        Directory existence is not enforced here.
        Creation is handled by export services.

    Args:
        output_directory:
            Target export directory.

    Returns:
        Tuple:
            (is_valid, message)
    """

    if not output_directory:
        return (
            False,
            "Export directory cannot be empty.",
        )

    path = Path(output_directory)

    if path.name.strip() == "":
        return (
            False,
            "Invalid export directory path.",
        )

    return True, "Valid export directory."


def validate_filename_pattern(
    pattern: str,
) -> tuple[bool, str]:
    """
    Validate export filename pattern.

    Supported placeholders:
        {title}
        {timestamp}

    Args:
        pattern:
            Filename template.

    Returns:
        Tuple:
            (is_valid, message)
    """

    if not pattern:
        return (
            False,
            "Filename pattern cannot be empty.",
        )

    if len(pattern) > MAX_FILENAME_PATTERN_LENGTH:
        return (
            False,
            "Filename pattern is too long.",
        )

    variables = set(
        re.findall(
            r"\{[^}]+\}",
            pattern,
        )
    )

    unsupported = variables - VALID_FILENAME_VARIABLES

    if unsupported:
        return (
            False,
            (
                "Unsupported filename variables: "
                f"{', '.join(sorted(unsupported))}"
            ),
        )

    return True, "Valid filename pattern."


def validate_boolean_option(
    value: bool,
    option_name: str,
) -> tuple[bool, str]:
    """
    Validate boolean settings.

    Args:
        value:
            Boolean option value.

        option_name:
            Display name.

    Returns:
        Tuple:
            (is_valid, message)
    """

    if not isinstance(value, bool):
        return (
            False,
            f"{option_name} must be enabled or disabled.",
        )

    return True, f"Valid {option_name} option."


# ---------------------------------------------------------------------------
# Composite Validator
# ---------------------------------------------------------------------------


def validate_export_settings(
    settings: dict,
) -> tuple[bool, list[str]]:
    """
    Validate complete export configuration.

    Args:
        settings:
            Export settings dictionary.

    Returns:
        Tuple:
            (
                is_valid,
                list_of_errors
            )
    """

    errors: list[str] = []

    checks = [
        validate_export_format(
            settings.get("export_format")
        ),
        validate_output_directory(
            settings.get("output_directory", "")
        ),
        validate_filename_pattern(
            settings.get("file_naming_pattern", "")
        ),
        validate_boolean_option(
            settings.get(
                "include_metadata"
            ),
            "Metadata inclusion",
        ),
        validate_boolean_option(
            settings.get(
                "include_summary"
            ),
            "Summary inclusion",
        ),
        validate_boolean_option(
            settings.get(
                "include_citations"
            ),
            "Citation inclusion",
        ),
    ]

    for valid, message in checks:
        if not valid:
            errors.append(message)

    return (
        len(errors) == 0,
        errors,
    )