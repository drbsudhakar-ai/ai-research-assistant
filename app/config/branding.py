"""
Central product identity for the AI Research Assistant.

UI pages and downloadable reports must consume this module rather than
hard-coding application name, author credit, or document titles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

APPLICATION_NAME: Final[str] = "AI Research Assistant"
TAGLINE: Final[str] = "Research-paper intelligence for academic users."
AUTHOR: Final[str] = "Dr. B. Sudhakar"
CREDIT: Final[str] = "Developed by Dr. B. Sudhakar"
COPYRIGHT: Final[str] = "© 2026 Dr. B. Sudhakar"
ICON: Final[str] = "📚"
VERSION: Final[str] = "1.0.1"
DOCUMENT_TITLE: Final[str] = "Research Paper Analysis Report"

# No logo/favicon files exist in the repository. Pages use ICON as a
# minimal placeholder. Do not invent institutional marks.
LOGO_PATH: Final[str | None] = None


@dataclass(frozen=True, slots=True)
class BrandConfig:
    """Single source of truth for product branding and document metadata."""

    application_name: str = APPLICATION_NAME
    tagline: str = TAGLINE
    author: str = AUTHOR
    credit: str = CREDIT
    copyright: str = COPYRIGHT
    icon: str = ICON
    version: str = VERSION
    document_title: str = DOCUMENT_TITLE
    logo_path: str | None = LOGO_PATH

    @property
    def page_title(self) -> str:
        return self.application_name

    @property
    def version_label(self) -> str:
        return f"v{self.version}"


_BRAND: Final[BrandConfig] = BrandConfig()


def get_brand_config() -> BrandConfig:
    """Return the process-wide branding configuration."""

    return _BRAND
