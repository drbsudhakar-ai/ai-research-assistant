"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/theme/theme_manager.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Theme orchestration manager for the AI Research Assistant UI.

    This module manages:
        - Active application theme
        - Light/Dark mode switching
        - Theme state persistence
        - CSS injection
        - Streamlit session integration

Architecture:
    UI Layer
        |
        |
    ThemeManager
        |
        +---- CSSBuilder
        |
        +---- Design Tokens
        |
        +---- Color Palette

===============================================================================
"""


from __future__ import annotations


from dataclasses import dataclass
from enum import StrEnum
from typing import Final


import streamlit as st


from app.ui.theme.css_builder import CSSBuilder



# =============================================================================
# Theme Definitions
# =============================================================================


class ThemeMode(StrEnum):
    """
    Supported application themes.
    """

    LIGHT = "light"

    DARK = "dark"



# =============================================================================
# Theme Configuration
# =============================================================================


@dataclass(
    frozen=True,
)
class ThemeConfig:
    """
    Theme configuration metadata.
    """

    name: str

    mode: ThemeMode

    description: str



# =============================================================================
# Available Themes
# =============================================================================


THEMES: Final[dict[ThemeMode, ThemeConfig]] = {

    ThemeMode.LIGHT:
        ThemeConfig(

            name="Light",

            mode=ThemeMode.LIGHT,

            description=
                "Professional light interface for research workflows.",

        ),


    ThemeMode.DARK:
        ThemeConfig(

            name="Dark",

            mode=ThemeMode.DARK,

            description=
                "Dark interface optimized for extended research sessions.",

        ),

}



# =============================================================================
# Theme Manager
# =============================================================================


class ThemeManager:
    """
    Central theme management service.

    Example:

        ThemeManager.initialize()

        ThemeManager.set_theme(
            ThemeMode.DARK
        )

        ThemeManager.inject()

    """

    SESSION_KEY: Final[str] = "ui_theme"



    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    @classmethod
    def initialize(
        cls,
        default: ThemeMode = ThemeMode.LIGHT,
    ) -> None:
        """
        Initialize theme state.

        Args:
            default:
                Default application theme.
        """

        if cls.SESSION_KEY not in st.session_state:

            st.session_state[
                cls.SESSION_KEY
            ] = default.value



    # -------------------------------------------------------------------------
    # Current Theme
    # -------------------------------------------------------------------------

    @classmethod
    def current_theme(cls) -> ThemeMode:
        """
        Return active theme.

        Returns:
            ThemeMode
        """

        cls.initialize()


        return ThemeMode(
            st.session_state[
                cls.SESSION_KEY
            ]
        )



    # -------------------------------------------------------------------------
    # Theme Setter
    # -------------------------------------------------------------------------

    @classmethod
    def set_theme(
        cls,
        theme: ThemeMode,
    ) -> None:
        """
        Change active theme.

        Args:
            theme:
                Selected theme mode.
        """

        cls.initialize()


        st.session_state[
            cls.SESSION_KEY
        ] = theme.value



    # -------------------------------------------------------------------------
    # Toggle Theme
    # -------------------------------------------------------------------------

    @classmethod
    def toggle(cls) -> ThemeMode:
        """
        Toggle between light and dark mode.

        Returns:
            ThemeMode:
                New active theme.
        """

        current = cls.current_theme()


        if current == ThemeMode.LIGHT:

            cls.set_theme(
                ThemeMode.DARK
            )

        else:

            cls.set_theme(
                ThemeMode.LIGHT
            )


        return cls.current_theme()



    # -------------------------------------------------------------------------
    # Theme Metadata
    # -------------------------------------------------------------------------

    @classmethod
    def config(cls) -> ThemeConfig:
        """
        Return current theme configuration.

        Returns:
            ThemeConfig
        """

        return THEMES[
            cls.current_theme()
        ]



    # -------------------------------------------------------------------------
    # Available Themes
    # -------------------------------------------------------------------------

    @classmethod
    def available_themes(
        cls,
    ) -> list[ThemeConfig]:
        """
        Return all available themes.

        Returns:
            list[ThemeConfig]
        """

        return list(
            THEMES.values()
        )



    # -------------------------------------------------------------------------
    # CSS Injection
    # -------------------------------------------------------------------------

    @classmethod
    def inject(
        cls,
    ) -> None:
        """
        Inject application CSS.

        This should be called once during app startup.
        """

        CSSBuilder.inject()



    # -------------------------------------------------------------------------
    # Theme Selector Component
    # -------------------------------------------------------------------------

    @classmethod
    def render_selector(
        cls,
    ) -> None:
        """
        Render theme selector widget.

        Used inside settings page/sidebar.
        """

        current = cls.current_theme()


        selected = st.selectbox(

            "Theme",

            options=[
                theme.value
                for theme in ThemeMode
            ],

            index=[
                theme.value
                for theme in ThemeMode
            ].index(
                current.value
            ),

        )


        if selected != current.value:

            cls.set_theme(
                ThemeMode(selected)
            )

            st.rerun()



    # -------------------------------------------------------------------------
    # Debug Information
    # -------------------------------------------------------------------------

    @classmethod
    def info(cls) -> dict:
        """
        Return theme diagnostic information.

        Returns:
            dict
        """

        theme = cls.config()


        return {

            "theme":
                theme.name,

            "mode":
                theme.mode.value,

            "description":
                theme.description,

            "available":
                [
                    item.name
                    for item in THEMES.values()
                ],

        }