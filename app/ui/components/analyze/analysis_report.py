"""
===============================================================================
Project      : AI Research Assistant
File         : analysis_report.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Analysis report display component.

Responsibilities:
    - Render completed research paper analysis.
    - Display metadata.
    - Display structured AI output.

Non-Responsibilities:
    - Running analysis pipeline.
    - Calling LLM services.
    - Saving history.
    - Export generation.

===============================================================================
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict


# ---------------------------------------------------------------------------
# Public Component
# ---------------------------------------------------------------------------


def render_analysis_report(
    record: Dict[str, Any] | None,
) -> None:
    """
    Render analysis report.

    Parameters
    ----------
    record:
        Analysis result dictionary.

    Returns
    -------
    None
    """

    if not record:
        st.info(
            "No analysis report available."
        )
        return


    st.divider()

    st.subheader(
        "📄 Research Analysis Report"
    )


    render_report_metadata(record)


    st.divider()


    render_report_content(record)



# ---------------------------------------------------------------------------
# Metadata Section
# ---------------------------------------------------------------------------


def render_report_metadata(
    record: Dict[str, Any],
) -> None:
    """
    Display paper and execution metadata.
    """

    columns = st.columns(4)


    with columns[0]:
        st.metric(
            "Pages",
            record.get(
                "pages",
                "-"
            ),
        )


    with columns[1]:
        st.metric(
            "Characters",
            record.get(
                "characters",
                "-"
            ),
        )


    with columns[2]:
        st.metric(
            "Provider",
            record.get(
                "provider",
                "-"
            ),
        )


    with columns[3]:
        st.metric(
            "Model",
            record.get(
                "model",
                "-"
            ),
        )


    title = record.get(
        "title"
    )

    if title:
        st.markdown(
            f"**Title:** {title}"
        )


    filename = record.get(
        "filename"
    )

    if filename:
        st.markdown(
            f"**File:** {filename}"
        )


    execution_time = record.get(
        "execution_time"
    )

    if execution_time:

        st.caption(
            f"Execution Time: {execution_time:.2f} seconds"
        )



# ---------------------------------------------------------------------------
# Report Content
# ---------------------------------------------------------------------------


def render_report_content(
    record: Dict[str, Any],
) -> None:
    """
    Display AI generated analysis content.
    """

    analysis = (
        record.get("analysis")
        or
        record.get("content")
        or
        record.get("report")
    )


    if not analysis:

        st.warning(
            "Analysis content is empty."
        )

        return


    with st.container():

        st.markdown(
            analysis
        )