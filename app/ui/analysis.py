"""
===========================================================
Project      : AI Research Assistant
File         : analysis.py
Version      : 0.3.0
Author       : Dr. B. Sudhakar

Description:
UI components for displaying AI-generated research paper
analysis.

This module is responsible ONLY for presentation.
It does NOT communicate with the LLM.
===========================================================
"""

import streamlit as st
from app.config.llm_config import LLMConfig



def render_analysis(
    result: str,
    execution_time: float
) -> None:
    """
    Display the AI-generated analysis.

    Parameters
    ----------
    result : str
        Markdown formatted analysis returned by the PaperAnalyzer.
    execution_time : float
        Time taken by the LLM to generate the analysis.
    """
    config = LLMConfig()

    st.success("✅ Analysis completed successfully.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🤖 Model", config.MODEL_NAME)

    with col2:
        st.metric("🦙 Provider", config.PROVIDER)

    with col3:
        st.metric(
            "⏱ Time",
            f"{execution_time:.2f} sec"
        )

    with col4:
        st.metric(
            "📄 Report Size",
            f"{len(result):,} chars"
        )

    st.divider()

    st.markdown("## 📊 Research Paper Analysis Report")

    st.markdown(result)

    st.divider()

    st.download_button(
        label="📥 Download Report (.md)",
        data=result,
        file_name="research_paper_analysis.md",
        mime="text/markdown",
        use_container_width=True,
    )