"""
===============================================================================
Project      : AI Research Assistant
File         : history.py
Version      : 0.4.0
Author       : Dr. B. Sudhakar

Description:
User interface for viewing and managing previously analyzed
research papers stored in the SQLite database.
===============================================================================
"""

import streamlit as st

from app.services.history_service import HistoryService


def show_history_page():
    """
    Display analysis history.
    """

    st.header("📜 Analysis History")

    st.caption(
        "Browse previously analyzed research papers."
    )

    st.divider()

    history_service = HistoryService()

    records = history_service.get_all_analyses()
    
    if not records:

        st.info(
            "No analysis history found."
        )

        return 

    st.info(
    f"Showing {len(records)} saved analyses."
    )

    st.divider()

    for record in records:

        with st.container(border=True):

            st.subheader(record.title)
            

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Analysis Type:** {record.analysis_type}")
                st.write(f"**Model:** {record.model}")
                st.write(f"**Provider:** {record.provider}")

            with col2:
                st.write(
                    f"**Execution Time:** "
                    f"{record.execution_time:.2f} sec"
                )
                st.write(
                    f"**Input Source:** "
                    f"{record.input_source.upper()}"
                )
                st.caption(f"📅 {record.created_at}")
                
    
            st.divider()
            button_col1, button_col2 = st.columns(2)

            with button_col1:

                if st.button(
                    "👁 View Report",
                    key=f"view_{record.id}",
                    use_container_width=True,
                ):

                    st.session_state["analysis_record"] = record

                    st.rerun()

            with button_col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{record.id}",
                    use_container_width=True,
                ):

                    st.warning(
                        "Delete functionality will be added "
                        "in Version 0.4.1"
                    )
            st.markdown("")