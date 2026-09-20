"""
Export Settings UI Defaults

Defines default values used by the Export Settings UI layer.

Responsibilities:
- Provide initial export configuration values
- Provide safe application defaults
- Keep UI initialization independent from business logic

Does NOT contain:
- Validation rules
- File generation logic
- Export services
- Persistence handling

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass

from app.ui.components.settings.export.enums import (
    ExportFormat,
)


@dataclass(frozen=True)
class ExportSettingsDefaults:
    """
    Default export configuration values.

    These values are used when:
    - User opens Export Settings for the first time
    - No saved configuration exists
    - Settings state needs initialization
    """

    export_format: ExportFormat = ExportFormat.PDF

    include_metadata: bool = True

    include_summary: bool = True

    include_citations: bool = True

    output_directory: str = "exports"

    file_naming_pattern: str = (
        "{title}_{timestamp}"
    )


class DefaultExportSettings:
    """
    Registry for export UI default values.

    Provides a centralized source for defaults
    consumed by settings state initialization.
    """

    VALUES = ExportSettingsDefaults()

    @classmethod
    def get(cls) -> ExportSettingsDefaults:
        """
        Return default export settings.

        Returns:
            ExportSettingsDefaults instance
        """

        return cls.VALUES

    @classmethod
    def as_dict(cls) -> dict[str, object]:
        """
        Return defaults as dictionary.

        Useful for:
        - Session state initialization
        - Configuration merging
        - Serialization

        Returns:
            Dictionary containing default settings
        """

        settings = cls.VALUES

        return {
            "export_format": settings.export_format,
            "include_metadata": settings.include_metadata,
            "include_summary": settings.include_summary,
            "include_citations": settings.include_citations,
            "output_directory": settings.output_directory,
            "file_naming_pattern": settings.file_naming_pattern,
        }