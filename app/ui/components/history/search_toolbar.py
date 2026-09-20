"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/history/search_toolbar.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable search toolbar component for the Analysis History page.
===============================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
import streamlit as st

@dataclass(slots=True)
class SearchToolbarState:
    query: str
    refresh_requested: bool = False
    clear_requested: bool = False

class SearchToolbar:
    """Reusable history search toolbar."""

    def __init__(
        self,
        *,
        placeholder: str = "Search by title, filename, author...",
        key: str = "history_search",
        disabled: bool = False,
    ) -> None:
        self.placeholder = placeholder
        self.key = key
        self.disabled = disabled

    def render(self, *, result_count: int | None = None) -> SearchToolbarState:
        c1, c2, c3 = st.columns([6,1,1])

        with c1:
            query = st.text_input(
                "Search",
                key=self.key,
                placeholder=self.placeholder,
                label_visibility="collapsed",
                disabled=self.disabled,
            )

        with c2:
            refresh = st.button("Refresh", key=f"{self.key}_refresh", use_container_width=True)

        with c3:
            clear = st.button("Clear", key=f"{self.key}_clear", use_container_width=True)

        if clear:
            st.session_state[self.key] = ""
            query = ""

        if result_count is not None:
            st.caption(f"{result_count:,} record(s)")

        return SearchToolbarState(
            query=query.strip(),
            refresh_requested=refresh,
            clear_requested=clear,
        )

__all__ = ["SearchToolbar", "SearchToolbarState"]
