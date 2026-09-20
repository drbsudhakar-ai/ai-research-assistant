# =============================================================================
# File: app/config/export_config.py
# Production Ready Export Configuration Layer
# Version: 1.0.0
# =============================================================================

from __future__ import annotations


from dataclasses import (
    dataclass,
    field,
    asdict,
)


from typing import (
    Any,
)


from pathlib import Path


import logging


logger = logging.getLogger(
    __name__
)



# =============================================================================
# Export Format Configuration
# =============================================================================


@dataclass
class ExportFormatConfig:
    """
    Individual export format settings.

    Supported formats:

        PDF
        Markdown
        DOCX
        HTML
    """

    enabled: bool = True

    include_title: bool = True

    include_metadata: bool = True

    include_sections: bool = True

    include_references: bool = True



# =============================================================================
# Citation Configuration
# =============================================================================


@dataclass
class CitationConfig:
    """
    Citation formatting configuration.
    """

    enabled: bool = True

    style: str = (
        "APA"
    )

    include_bibliography: bool = True

    include_inline_citations: bool = True



    def validate(
        self,
    ) -> tuple[bool, str]:
        """
        Validate citation settings.
        """

        supported_styles = (

            "APA",

            "IEEE",

            "MLA",

            "Chicago",

        )


        if self.style not in supported_styles:

            return (

                False,

                (
                    "Unsupported citation style."
                ),

            )


        return (

            True,

            "Citation configuration valid.",

        )



# =============================================================================
# Report Template Configuration
# =============================================================================


@dataclass
class ReportTemplateConfig:
    """
    Report template settings.
    """

    template_name: str = (
        "research_standard"
    )


    include_sections: list[str] = field(

        default_factory=lambda: [

            "abstract",

            "introduction",

            "research_gap",

            "methodology",

            "results",

            "contributions",

            "limitations",

            "future_work",

            "references",

        ]

    )


    custom_footer: str = ""



# =============================================================================
# File Naming Configuration
# =============================================================================


@dataclass
class FileNamingConfig:
    """
    Output file naming rules.
    """

    prefix: str = (
        "analysis"
    )


    include_timestamp: bool = True


    include_model_name: bool = True



    extension_separator: str = "."



    def generate_filename(
        self,
        title: str,
        extension: str,
        model: str | None = None,
    ) -> str:
        """
        Generate export filename.
        """

        parts = [

            self.prefix,

        ]


        if title:

            safe_title = (

                title
                .lower()
                .replace(
                    " ",
                    "_",
                )

            )

            parts.append(
                safe_title
            )


        if self.include_model_name and model:

            parts.append(
                model.replace(
                    ":",
                    "_",
                )
            )


        filename = (
            "_".join(parts)
        )


        return (
            filename
            +
            self.extension_separator
            +
            extension
        )



# =============================================================================
# Main Export Configuration
# =============================================================================


@dataclass
class ExportConfig:
    """
    Complete export configuration.
    """

    output_directory: str = (
        "exports"
    )


    pdf: ExportFormatConfig = field(

        default_factory=ExportFormatConfig

    )


    markdown: ExportFormatConfig = field(

        default_factory=ExportFormatConfig

    )


    docx: ExportFormatConfig = field(

        default_factory=ExportFormatConfig

    )


    html: ExportFormatConfig = field(

        default_factory=ExportFormatConfig

    )


    citation: CitationConfig = field(

        default_factory=CitationConfig

    )


    template: ReportTemplateConfig = field(

        default_factory=ReportTemplateConfig

    )


    naming: FileNamingConfig = field(

        default_factory=FileNamingConfig

    )


    create_research_summary: bool = True


    create_executive_summary: bool = True



    def validate(
        self,
    ) -> tuple[bool, list[str]]:
        """
        Validate export configuration.
        """

        errors = []


        valid, message = (

            self.citation.validate()

        )


        if not valid:

            errors.append(
                message
            )


        if not self.output_directory:

            errors.append(

                "Output directory cannot be empty."

            )


        return (

            len(errors) == 0,

            errors,

        )



    def get_output_path(
        self,
    ) -> Path:
        """
        Return export directory path.
        """

        path = Path(

            self.output_directory

        )


        path.mkdir(

            parents=True,

            exist_ok=True,

        )


        return path



    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert configuration to dictionary.
        """

        return asdict(
            self
        )



# =============================================================================
# Default Export Configuration
# =============================================================================


def create_default_export_config(
) -> ExportConfig:
    """
    Create default research export settings.
    """

    return ExportConfig()



# =============================================================================
# Global Default Instance
# =============================================================================


DEFAULT_EXPORT_CONFIG = (
    create_default_export_config()
)



__all__ = [

    "ExportFormatConfig",

    "CitationConfig",

    "ReportTemplateConfig",

    "FileNamingConfig",

    "ExportConfig",

    "DEFAULT_EXPORT_CONFIG",

    "create_default_export_config",

]