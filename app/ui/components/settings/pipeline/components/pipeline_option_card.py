"""
AI Research Assistant

File: app/ui/components/settings/pipeline/components/pipeline_option_card.py
Pipeline Settings - Pipeline Option Card Component

Reusable card component for displaying selectable
pipeline configuration options.

Used for:
    - Analysis Mode
    - Execution Mode
    - LLM Strategy
    - Retry Policy
    - Progress Mode
    - Performance Options

Responsibilities:
    - Consistent visual presentation
    - Display metadata
    - Handle selection state

No business logic.
No pipeline execution.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from dataclasses import dataclass


# ============================================================
# Data Model
# ============================================================


@dataclass(frozen=True)
class OptionCardData:
    """
    Data model for option cards.
    """

    label: str

    description: str

    help_text: str

    icon: str | None = None



class PipelineOptionCard:
    """
    Generic selectable option card.

    Supports:
        - radio selection
        - single choice configuration
        - metadata driven UI
    """


    def __init__(
        self,
        title: str,
        options: list,
        selected,
        metadata_map: dict,
        key: str,
        horizontal: bool = False,
    ) -> None:
        """
        Initialize option card.

        Args:
            title:
                Card title.

            options:
                Enum values.

            selected:
                Current selected value.

            metadata_map:
                Enum -> metadata mapping.

            key:
                Streamlit unique key.

            horizontal:
                Radio layout direction.
        """

        self.title = title

        self.options = options

        self.selected = selected

        self.metadata_map = metadata_map

        self.key = key

        self.horizontal = horizontal


    # ========================================================
    # Render
    # ========================================================

    def render(self):
        """
        Render option card.

        Returns:
            Selected option.
        """

        st.markdown(
            f"#### {self.title}"
        )


        labels = {
            option:
                self._format_option(
                    option
                )
            for option in self.options
        }


        selected = st.radio(
            label=self.title,
            options=self.options,
            index=self.options.index(
                self.selected
            ),
            format_func=lambda item:
                labels[item],
            horizontal=self.horizontal,
            key=self.key,
        )


        self._render_description(
            selected
        )


        return selected


    # ========================================================
    # Helpers
    # ========================================================

    def _format_option(
        self,
        option,
    ) -> str:
        """
        Format option display.
        """

        metadata = (
            self.metadata_map[
                option
            ]
        )


        if metadata.icon:

            return (
                f"{metadata.icon} "
                f"{metadata.label}"
            )


        return metadata.label



    def _render_description(
        self,
        selected,
    ) -> None:
        """
        Display selected option details.
        """

        metadata = (
            self.metadata_map[
                selected
            ]
        )


        st.caption(
            metadata.description
        )


        if metadata.help_text:

            st.info(
                metadata.help_text
            )


__all__ = [
    "PipelineOptionCard",
    "OptionCardData",
]