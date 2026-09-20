"""
===========================================================
Project      : AI Research Assistant
File         : components.py
Version      : 0.4.0
Author       : Dr. B. Sudhakar

Description:
Reusable UI components.

This module contains reusable Streamlit UI components
used throughout the application.
===========================================================
"""

import streamlit as st

from app.utils.pdf_extractor import PDFExtractor


# ==========================================================
# INPUT SECTION
# ==========================================================

def render_input_section() -> dict:
    """
    Render the research paper input section.

    Users can either:
    - Upload a PDF
    - Paste research paper text

    Returns
    -------
    dict
        Dictionary containing:

        title : str
            Paper title or filename.

        filename : str
            Uploaded filename.

        input_source : str
            "pdf" or "text"

        paper_text : str
            Extracted or pasted paper text.
    """

    st.subheader("📥 Input Research Paper")

    input_method = st.radio(
        "Select Input Method",
        (
            "Upload PDF",
            "Paste Research Paper Text",
        ),
    )

    # ------------------------------------------------------
    # Default values
    # ------------------------------------------------------

    paper_text = ""
    paper_title = "Manual Text Input"
    filename = ""
    input_source = "text"

    # ------------------------------------------------------
    # PDF Upload
    # ------------------------------------------------------

    if input_method == "Upload PDF":

        uploaded_file = st.file_uploader(
            "Choose Research Paper (PDF)",
            type=["pdf"],
        )

        if uploaded_file is not None:

            paper_title = uploaded_file.name
            filename = uploaded_file.name
            input_source = "pdf"

            (
                paper_text,
                total_pages,
                total_characters,
            ) = PDFExtractor.extract_text(uploaded_file)

            st.success("✅ PDF loaded successfully.")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("📄 Pages", total_pages)

            with col2:
                st.metric("🔤 Characters", f"{total_characters:,}")

            with st.expander("📄 Extracted Text Preview"):

                st.text_area(
                    "Extracted Text",
                    value=paper_text,
                    height=300,
                    label_visibility="collapsed",
                )

    # ------------------------------------------------------
    # Manual Text Input
    # ------------------------------------------------------

    else:

        paper_text = st.text_area(
            "Paste Research Paper",
            height=350,
            placeholder="Paste the research paper text here...",
        )

    # ------------------------------------------------------
    # Return metadata
    # ------------------------------------------------------

    return {
        "title": paper_title,
        "filename": filename,
        "input_source": input_source,
        "paper_text": paper_text,
    }