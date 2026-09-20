"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme System
File         : app/ui/theme/components.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Component-level design tokens for the Streamlit UI.

    Defines reusable visual specifications for:
    - Cards
    - Buttons
    - Metrics
    - Alerts
    - Upload containers
    - Analysis result panels
    - Tables
    - Badges

Purpose:
    - Provide a consistent component design language.
    - Avoid repeated CSS values across UI pages.
    - Support professional academic dashboard styling.

Dependencies:
    Internal:
        - app.ui.theme.design_tokens
        - app.ui.theme.color_palette
        - app.ui.theme.spacing
        - app.ui.theme.typography

    External:
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.theme.components import COMPONENTS

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from app.ui.theme.design_tokens import TOKENS
from app.ui.theme.spacing import SPACING
from app.ui.theme.typography import TYPOGRAPHY


@dataclass(frozen=True)
class CardTokens:
    """
    Card component styling tokens.

    Used for:
    - Dashboard cards
    - Analysis result sections
    - History items
    - Information panels
    """

    BACKGROUND: str = TOKENS.COLORS.SURFACE

    BORDER: str = TOKENS.COLORS.BORDER

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_LARGE

    PADDING: str = SPACING.COMPONENTS.CARD_PADDING

    SHADOW: str = TOKENS.SHADOWS.MEDIUM

    HEADER_GAP: str = SPACING.COMPONENTS.CARD_HEADER_GAP

    CONTENT_GAP: str = SPACING.COMPONENTS.CARD_CONTENT_GAP


@dataclass(frozen=True)
class ButtonTokens:
    """
    Button component styling tokens.
    """

    HEIGHT: str = TOKENS.COMPONENTS.BUTTON_HEIGHT

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_MEDIUM

    FONT_SIZE: str = TYPOGRAPHY.FONT_SIZE.BODY

    FONT_WEIGHT: int = TYPOGRAPHY.FONT_WEIGHT.MEDIUM

    PADDING_VERTICAL: str = (
        SPACING.COMPONENTS.BUTTON_PADDING_VERTICAL
    )

    PADDING_HORIZONTAL: str = (
        SPACING.COMPONENTS.BUTTON_PADDING_HORIZONTAL
    )


@dataclass(frozen=True)
class MetricCardTokens:
    """
    Metric display card tokens.

    Used for:
    - Number of papers analyzed
    - Processing statistics
    - Dashboard KPIs
    """

    BACKGROUND: str = TOKENS.COLORS.SURFACE

    VALUE_SIZE: str = TYPOGRAPHY.FONT_SIZE.XXL

    LABEL_SIZE: str = TYPOGRAPHY.FONT_SIZE.SMALL

    VALUE_WEIGHT: int = TYPOGRAPHY.FONT_WEIGHT.BOLD

    LABEL_WEIGHT: int = TYPOGRAPHY.FONT_WEIGHT.NORMAL

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_LARGE

    PADDING: str = SPACING.COMPONENTS.CARD_PADDING


@dataclass(frozen=True)
class AlertTokens:
    """
    Alert and notification component tokens.

    Used for:
    - Success messages
    - Errors
    - Warnings
    - Information messages
    """

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_MEDIUM

    PADDING: str = SPACING.SCALE.MD

    FONT_SIZE: str = TYPOGRAPHY.FONT_SIZE.BODY

    FONT_WEIGHT: int = TYPOGRAPHY.FONT_WEIGHT.MEDIUM


@dataclass(frozen=True)
class UploadAreaTokens:
    """
    PDF upload component styling.

    Used in:
    - Analyze Paper page
    """

    BACKGROUND: str = TOKENS.COLORS.SURFACE

    BORDER: str = TOKENS.COLORS.BORDER

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_LARGE

    PADDING: str = SPACING.SCALE.XL

    TEXT_SIZE: str = TYPOGRAPHY.FONT_SIZE.BODY


@dataclass(frozen=True)
class ResultPanelTokens:
    """
    Analysis result display styling.

    Used for:
    - AI generated analysis
    - Research findings
    - Summary reports
    """

    BACKGROUND: str = TOKENS.COLORS.SURFACE

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_LARGE

    BORDER: str = TOKENS.COLORS.BORDER

    PADDING: str = SPACING.COMPONENTS.CARD_PADDING

    TITLE_SIZE: str = TYPOGRAPHY.FONT_SIZE.LARGE

    BODY_SIZE: str = TYPOGRAPHY.FONT_SIZE.BODY


@dataclass(frozen=True)
class TableTokens:
    """
    Data table styling tokens.

    Used for:
    - Analysis history
    - Research metadata
    """

    HEADER_SIZE: str = TYPOGRAPHY.FONT_SIZE.SMALL

    CELL_SIZE: str = TYPOGRAPHY.FONT_SIZE.BODY

    CELL_PADDING: str = SPACING.SCALE.SM

    BORDER: str = TOKENS.COLORS.BORDER


@dataclass(frozen=True)
class BadgeTokens:
    """
    Badge / tag component tokens.
    """

    BORDER_RADIUS: str = TOKENS.BORDERS.RADIUS_ROUNDED

    PADDING: str = SPACING.COMPONENTS.BADGE_PADDING

    FONT_SIZE: str = TYPOGRAPHY.FONT_SIZE.SMALL

    FONT_WEIGHT: int = TYPOGRAPHY.FONT_WEIGHT.MEDIUM


@dataclass(frozen=True)
class ComponentTokens:
    """
    Root component token container.
    """

    CARD: Final = CardTokens()

    BUTTON: Final = ButtonTokens()

    METRIC_CARD: Final = MetricCardTokens()

    ALERT: Final = AlertTokens()

    UPLOAD_AREA: Final = UploadAreaTokens()

    RESULT_PANEL: Final = ResultPanelTokens()

    TABLE: Final = TableTokens()

    BADGE: Final = BadgeTokens()


# Global component token instance
COMPONENTS: Final = ComponentTokens()