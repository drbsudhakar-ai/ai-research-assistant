"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Base Framework
File         : card_component.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Base class for all card-based UI components.

Responsibilities:
    - Store common card properties.
    - Validate card configuration.
    - Provide common rendering lifecycle.
    - Support future extensions.

Non-Responsibilities:
    - Render specific card content.
    - Business logic.
    - Data access.

===============================================================================
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from app.ui.base.component import UIComponent


@dataclass(slots=True)
class CardComponent(UIComponent):
    """
    Base class for all reusable card components.
    """

    title: str

    subtitle: str | None = None

    icon: str | None = None

    css_class: str = "card"

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """
        Validate card configuration.
        """

        if not self.title.strip():
            raise ValueError(
                "Card title cannot be empty."
            )

    @abstractmethod
    def render(self) -> None:
        """
        Render the card.
        """
        raise NotImplementedError