"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Report Viewer
File         : analyze_report.py

Description:
    Displays final AI-generated research paper analysis report.

Responsibilities:
    - Render analysis output
    - Display structured sections
    - Handle different result schemas safely
    - Provide report export placeholders

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Any

import streamlit as st



# =============================================================================
# Helpers
# =============================================================================


def _extract_analysis_text(
    result: Any,
) -> str:
    """
    Extract analysis text from different result formats.
    """

    if result is None:

        return ""



    if isinstance(
        result,
        str,
    ):

        return result



    possible_fields = [

        "analysis",

        "content",

        "report",

        "summary",

        "text",

        "output",

    ]


    for field in possible_fields:

        value = getattr(
            result,
            field,
            None,
        )


        if value:

            return str(value)



    if isinstance(
        result,
        dict,
    ):

        for field in possible_fields:

            if field in result:

                return str(
                    result[field]
                )



    return str(result)



def _extract_metadata(
    result: Any,
) -> dict[str, Any]:
    """
    Extract execution metadata.
    """

    metadata = {}


    if isinstance(
        result,
        dict,
    ):

        metadata = result.get(
            "metadata",
            {},
        )


    else:

        metadata = getattr(
            result,
            "metadata",
            {},
        )


    if metadata is None:

        metadata = {}


    return metadata



# =============================================================================
# Report Renderer
# =============================================================================


def render_analysis_report(
    analysis_result: Any | None,
) -> None:
    """
    Render completed analysis report.

    Args:
        analysis_result:
            Result returned by AnalysisService.
    """

    if analysis_result is None:

        st.info(
            "Analysis report will appear after completion."
        )

        return



    st.subheader(
        "🧠 AI Research Analysis Report"
    )



    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    metadata = _extract_metadata(
        analysis_result
    )


    if metadata:


        with st.expander(
            "📊 Analysis Metadata",
            expanded=False,
        ):

            for key, value in metadata.items():

                st.write(
                    f"**{key}:** {value}"
                )



    st.divider()



    # -------------------------------------------------------------------------
    # Main Report
    # -------------------------------------------------------------------------

    report_text = _extract_analysis_text(
        analysis_result
    )


    if report_text:


        st.markdown(
            report_text
        )


    else:

        st.warning(
            "No analysis content available."
        )



    st.divider()



    # -------------------------------------------------------------------------
    # Export Section
    # -------------------------------------------------------------------------

    _render_export_section(
        report_text
    )



# =============================================================================
# Export UI
# =============================================================================


def _render_export_section(
    report_text: str,
) -> None:
    """
    Render report download options.

    Actual converters can be connected later.
    """

    st.subheader(
        "📥 Export Report"
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        st.download_button(

            label="⬇️ Download Markdown",

            data=report_text,

            file_name="research_analysis.md",

            mime="text/markdown",

        )



    with col2:

        st.download_button(

            label="⬇️ Download Text",

            data=report_text,

            file_name="research_analysis.txt",

            mime="text/plain",

        )



    with col3:

        st.download_button(

            label="📄 PDF / DOCX",

            data="Export engine integration pending",

            file_name="export_status.txt",

            mime="text/plain",

        )