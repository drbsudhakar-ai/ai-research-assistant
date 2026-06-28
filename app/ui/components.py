"""
===========================================================
Project      : AI Research Assistant
File         : components.py
Version      : 0.3.0
Author       : Dr. B. Sudhakar
===========================================================
"""

import streamlit as st
from app.utils.pdf_extractor import PDFExtractor


# =========================================================
# INPUT SECTION
# =========================================================

def render_input_section():
    """
    Render PDF upload / text input section.

    Returns
    -------
    str
        Research paper text.
    """

    st.subheader("📥 Input Research Paper")

    input_method = st.radio(
        "Select Input Method",
        (
            "Upload PDF",
            "Paste Research Paper Text"
        )
    )

    paper_text = ""

    if input_method == "Upload PDF":

        uploaded_file = st.file_uploader(
            "Choose Research Paper (PDF)",
            type=["pdf"]
        )

        if uploaded_file is not None:

            (
                paper_text,
                total_pages,
                total_characters
            ) = PDFExtractor.extract_text(uploaded_file)

            st.success("PDF loaded successfully.")

            c1, c2 = st.columns(2)

            with c1:
                st.metric("Pages", total_pages)

            with c2:
                st.metric("Characters", total_characters)

            with st.expander("📄 Extracted Text Preview"):

                st.text_area(
                    "Extracted Text",
                    value=paper_text,
                    height=300,
                    label_visibility="collapsed"
                )

    else:

        paper_text = st.text_area(
            "Paste Research Paper",
            height=350,
            placeholder="Paste research paper here..."
        )

    return paper_text


# =========================================================
# ANALYSIS OUTPUT
# =========================================================

def render_analysis(result):

    st.success("Analysis completed successfully.")

    st.divider()

    st.markdown(result)
