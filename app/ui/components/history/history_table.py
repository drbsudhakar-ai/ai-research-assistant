from __future__ import annotations

from app.services.history_service import HistoryService
from app.config.navigation_config import PageKey
from app.core.session import set_session_value
"""Production-ready History Table."""
from collections.abc import Sequence
from html import escape
import streamlit as st
from app.ui.html_renderer import render_html
class HistoryTable:
    def render(self,records:Sequence[dict])->dict|None:
        if not records:
            st.info("No analysis history found."); return None
        event=None
        for i,r in enumerate(records):
            with st.container(border=True):
                render_html(f"""
                    <div class="ara-history-title">{escape(str(r.get('title','Untitled')))}</div>
                    <div class="ara-history-meta">
                        <span class="ara-chip">AI: {escape(str(r.get('provider','')).title())}</span>
                        <span class="ara-chip">Model: {escape(str(r.get('model','N/A')))}</span>
                        <span class="ara-chip">Created: {escape(str(r.get('created_at','N/A')))}</span>
                    </div>
                """)
                c1,c2,c3=st.columns(3)
                if c1.button("Open report",key=f"v{i}",use_container_width=True): event={"action":"view","record":r}
                if c2.button("Run analysis again",key=f"re{i}",use_container_width=True): event={"action":"reanalyze","record":r}
                if c3.button("Delete",key=f"d{i}",use_container_width=True): event={"action":"delete","record":r}
        return event


    @staticmethod
    def _handle_table_event(
        event: dict | None,
    ) -> None:

        if not event:
            return


        action = event["action"]


        record = event["record"]


        if action == "view":

            st.session_state["selected_record"] = record
            set_session_value("current_page", PageKey.REPORT)
            st.rerun()


        elif action == "delete":

            service = HistoryService()

            service.delete_analysis(
                record["id"]
            )

            st.success(
                "Analysis deleted."
            )

            st.rerun()


        elif action == "reanalyze":

            st.session_state["reanalyze_record"] = record
            set_session_value("current_page", PageKey.ANALYZE)
            st.rerun()
__all__=["HistoryTable"]
