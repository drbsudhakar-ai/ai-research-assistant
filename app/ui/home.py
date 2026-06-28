"""
home.py
----------------------------------------
Home page components for AI Research Assistant

Author  : Dr. B. Sudhakar
Version : 0.3.0
"""

import streamlit as st


def render_home():
    """
    Render the home page header.
    """

    st.markdown(
        """
        <div class="hero-title">
            📚 AI Research Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Your Intelligent Research Companion
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        """
Analyze research papers with **PhD-level academic rigor** using
Large Language Models.

This assistant helps researchers, faculty members, and postgraduate
students understand research papers, identify research gaps,
critically evaluate methodology, and generate future research ideas.
"""
    )

    st.markdown("---")

    # ============================================================
    # Feature Cards
    # ============================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            """
📄 **Paper Analysis**

• Abstract Summary

• Research Objectives

• Methodology Review

• Key Results

• Conclusion
"""
        )

    with col2:
        st.success(
            """
🔬 **Research Insights**

• Research Gaps

• Future Work

• Strengths

• Limitations

• Critical Review
"""
        )

    with col3:
        st.warning(
            """
🤖 **AI Powered**

• Local LLM

• Privacy First

• Fast Analysis

• Modular Design

• Open Source
"""
        )

    st.markdown("---")