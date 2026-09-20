"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme System
File         : typography.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Typography system for the Streamlit UI.

    Defines:
    - Font families
    - Font sizes
    - Font weights
    - Text hierarchy
    - CSS typography helpers

Purpose:
    - Maintain consistent typography across all UI pages.
    - Provide professional academic application styling.
    - Avoid repeated inline CSS definitions.

Usage:
    from app.ui.theme.typography import Typography

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class FontFamily:
    """
    Font family definitions.
    """

    PRIMARY: str = (
        "Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    )

    MONOSPACE: str = (
        "JetBrains Mono, Consolas, Monaco, monospace"
    )


@dataclass(frozen=True)
class FontSize:
    """
    Application font scale.
    """

    XS: str = "0.75rem"

    SMALL: str = "0.875rem"

    BODY: str = "1rem"

    MEDIUM: str = "1.125rem"

    LARGE: str = "1.25rem"

    XL: str = "1.5rem"

    XXL: str = "2rem"

    DISPLAY: str = "2.5rem"


@dataclass(frozen=True)
class FontWeight:
    """
    Font weight scale.
    """

    LIGHT: int = 300

    NORMAL: int = 400

    MEDIUM: int = 500

    SEMIBOLD: int = 600

    BOLD: int = 700

    EXTRA_BOLD: int = 800


@dataclass(frozen=True)
class LineHeight:
    """
    Text line-height scale.
    """

    COMPACT: float = 1.25

    NORMAL: float = 1.5

    RELAXED: float = 1.75


@dataclass(frozen=True)
class TextStyle:
    """
    Semantic typography styles.

    These represent UI roles rather than HTML tags.
    """

    PAGE_TITLE: dict = None

    SECTION_TITLE: dict = None

    CARD_TITLE: dict = None

    BODY_TEXT: dict = None

    SECONDARY_TEXT: dict = None

    CAPTION: dict = None

    CODE: dict = None

    def __post_init__(self):
        object.__setattr__(
            self,
            "PAGE_TITLE",
            {
                "font-family": FontFamily.PRIMARY,
                "font-size": FontSize.DISPLAY,
                "font-weight": FontWeight.BOLD,
                "line-height": LineHeight.COMPACT,
            },
        )

        object.__setattr__(
            self,
            "SECTION_TITLE",
            {
                "font-family": FontFamily.PRIMARY,
                "font-size": FontSize.XXL,
                "font-weight": FontWeight.SEMIBOLD,
                "line-height": LineHeight.NORMAL,
            },
        )

        object.__setattr__(
            self,
            "CARD_TITLE",
            {
                "font-family": FontFamily.PRIMARY,
                "font-size": FontSize.LARGE,
                "font-weight": FontWeight.SEMIBOLD,
                "line-height": LineHeight.NORMAL,
            },
        )

        object.__setattr__(
            self,
            "BODY_TEXT",
            {
                "font-family": FontFamily.PRIMARY,
                "font-size": FontSize.BODY,
                "font-weight": FontWeight.NORMAL,
                "line-height": LineHeight.RELAXED,
            },
        )

        object.__setattr__(
            self,
            "SECONDARY_TEXT",
            {
                "font-family": FontFamily.PRIMARY,
                "font-size": FontSize.SMALL,
                "font-weight": FontWeight.NORMAL,
                "line-height": LineHeight.NORMAL,
            },
        )

        object.__setattr__(
            self,
            "CAPTION",
            {
                "font-family": FontFamily.PRIMARY,
                "font-size": FontSize.XS,
                "font-weight": FontWeight.NORMAL,
                "line-height": LineHeight.NORMAL,
            },
        )

        object.__setattr__(
            self,
            "CODE",
            {
                "font-family": FontFamily.MONOSPACE,
                "font-size": FontSize.SMALL,
                "font-weight": FontWeight.NORMAL,
                "line-height": LineHeight.NORMAL,
            },
        )


@dataclass(frozen=True)
class Typography:
    """
    Root typography configuration.
    """

    FONT_FAMILY: Final = FontFamily()

    FONT_SIZE: Final = FontSize()

    FONT_WEIGHT: Final = FontWeight()

    LINE_HEIGHT: Final = LineHeight()

    TEXT_STYLE: Final = TextStyle()


# Global typography instance
TYPOGRAPHY: Final = Typography()