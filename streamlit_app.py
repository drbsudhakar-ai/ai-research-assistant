"""
===============================================================================
Project      : AI Research Assistant
File         : streamlit_app.py
Version      : 0.3.0
Author       : Dr. B. Sudhakar
===============================================================================
"""

import streamlit as st
import time
from app.agents.paper_analyzer import PaperAnalyzer
from app.ui.styles import load_css
from app.ui.sidebar import render_sidebar
from app.ui.home import render_home

from app.ui.components import (
    render_input_section
)

from app.ui.footer import render_footer

from app.ui.analysis import render_analysis

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)

load_css()
render_sidebar()
render_home()

# st.divider()

paper_text = render_input_section()

# =============================================================================
# ANALYZE BUTTON
# =============================================================================

st.divider()

if st.button(
    "🔍 Analyze Paper",
    type="primary",
    use_container_width=True
):

    if not paper_text.strip():
        st.warning("Please upload a PDF or paste research paper text.")

    else:
        analyzer = PaperAnalyzer()

        with st.spinner("🤖 AI is analyzing the research paper..."):

            try:
                start_time = time.perf_counter()

                result = analyzer.analyze(paper_text)

                end_time = time.perf_counter()

                execution_time = end_time - start_time

                render_analysis(
                    result=result,
                    execution_time=execution_time
                )

            except Exception as e:
                st.error(str(e))
# =============================================================================
# FOOTER
# =============================================================================
render_footer()
