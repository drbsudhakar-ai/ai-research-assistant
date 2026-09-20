"""
Export Settings UI Metadata

Defines presentation metadata for export configuration components.

Responsibilities:
- UI labels
- Help text
- Descriptions
- Display ordering hints

Does NOT contain:
- Validation logic
- Default values
- Business rules
- Export implementation

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExportSettingMetadata:
    """
    Metadata definition for an export setting field.
    """

    label: str
    description: str
    help_text: str | None = None
    section: str = "Export"


class ExportMetadata:
    """
    Central registry for export settings UI metadata.

    Used by:
    - export_settings.py
    - export components
    - future dynamic settings renderer
    """

    FORMAT = ExportSettingMetadata(
        label="Export Format",
        description="Select the preferred output format for generated reports.",
        help_text=(
            "Choose how analysis reports should be exported. "
            "Supported formats include PDF, Markdown, DOCX, and HTML."
        ),
    )

    INCLUDE_METADATA = ExportSettingMetadata(
        label="Include Analysis Metadata",
        description=(
            "Include paper information, model details, execution time, "
            "and analysis statistics in exported reports."
        ),
        help_text=(
            "Adds technical metadata such as provider, model name, "
            "page count, and processing details."
        ),
    )

    INCLUDE_SUMMARY = ExportSettingMetadata(
        label="Include Executive Summary",
        description=(
            "Generate and include a concise executive summary section."
        ),
        help_text=(
            "Useful for quick review of research objectives, "
            "findings, and contributions."
        ),
    )

    INCLUDE_CITATIONS = ExportSettingMetadata(
        label="Include Citation Information",
        description=(
            "Include citation-ready information in exported documents."
        ),
        help_text=(
            "Adds reference information extracted from the research paper."
        ),
    )

    OUTPUT_DIRECTORY = ExportSettingMetadata(
        label="Export Location",
        description=(
            "Directory where generated reports will be stored."
        ),
        help_text=(
            "Specify the default location for exported research reports."
        ),
    )

    FILE_NAMING = ExportSettingMetadata(
        label="File Naming Pattern",
        description=(
            "Define naming rules for generated export files."
        ),
        help_text=(
            "Supports automatic naming using paper title and timestamp."
        ),
    )

    @classmethod
    def all(cls) -> dict[str, ExportSettingMetadata]:
        """
        Return all export metadata definitions.

        Returns:
            Mapping of setting keys to metadata objects.
        """

        return {
            "format": cls.FORMAT,
            "include_metadata": cls.INCLUDE_METADATA,
            "include_summary": cls.INCLUDE_SUMMARY,
            "include_citations": cls.INCLUDE_CITATIONS,
            "output_directory": cls.OUTPUT_DIRECTORY,
            "file_naming": cls.FILE_NAMING,
        }