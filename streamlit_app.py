"""
===============================================================================
Project      : AI Research Assistant
File         : streamlit_app.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar
===============================================================================
"""

import streamlit as st

from app.agents.paper_analyzer import PaperAnalyzer
from app.utils.pdf_extractor import PDFExtractor

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)

# =============================================================================
# HEADER
# =============================================================================

st.title("📚 AI Research Assistant")

st.write(
    """
Analyze research papers using AI with PhD-level academic rigor.

Developed by **Dr. B. Sudhakar**
"""
)

st.divider()

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    st.header("Project Information")

    st.write("Version : 1.0.0")

    st.write("Provider : Ollama")

    st.write("Model : qwen3:4b")

st.divider()

# =============================================================================
# INPUT METHOD
# =============================================================================

input_method = st.radio(
    "Select Input Method",
    (
        "Upload PDF",
        "Paste Research Paper Text"
    )
)

paper_text = ""

# =============================================================================
# PDF INPUT
# =============================================================================

if input_method == "Upload PDF":

    uploaded_file = st.file_uploader(
        "Choose a Research Paper (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        (
            paper_text,
            total_pages,
            total_characters
        ) = PDFExtractor.extract_text(uploaded_file)

        st.success("PDF loaded successfully.")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Pages", total_pages)

        with col2:
            st.metric("Characters", total_characters)

        with st.expander("Extracted Text Preview"):

            st.text_area(
               label="Extracted Paper Text",
               value=paper_text, 
               height=300,
               label_visibility="collapsed"
            )

# =============================================================================
# TEXT INPUT
# =============================================================================

else:

    paper_text = st.text_area(
       label="Paste Research Paper Text",
       height=350,
       placeholder="Paste your research paper here..."
    )

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

        st.warning("Please upload a PDF or paste paper text.")

    else:

        analyzer = PaperAnalyzer()

        with st.spinner("Analyzing Research Paper..."):

            try:

                result = analyzer.analyze(paper_text)

                st.success("Analysis completed successfully.")

                st.divider()

                st.markdown(result)

            except Exception as e:

                st.error(str(e))

# =============================================================================
# FOOTER
# =============================================================================

st.divider()

st.caption(
    "AI Research Assistant | Version 1.0.0"
)