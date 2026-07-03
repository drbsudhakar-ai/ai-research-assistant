"""
===============================================================================
Project      : AI Research Assistant
File         : analyze.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
Analyze Research Paper page.

Responsibilities:
    - Upload research papers.
    - Invoke the analysis service.
    - Display analysis results.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from app.utils.paper_preprocessor import PaperPreprocessor

from app.services.analysis_service import AnalysisService

from app.utils.pdf_text_formatter import PDFTextFormatter


def show_analyze_page() -> None:
    """
    Render the Analyze Research Paper page.
    """

    st.title("📄 Analyze Research Paper")

    st.write(
        "Upload a research paper in PDF format and generate an "
        "AI-powered analysis."
    )

    uploaded_file = st.file_uploader(
        label="Choose a PDF file",
        type=["pdf"],
        accept_multiple_files=False,
    )

    if uploaded_file is None:
        st.info("Please upload a research paper to begin.")
        return

    st.success(f"Selected file: **{uploaded_file.name}**")

    preprocessor = PaperPreprocessor()

    try:
        paper = preprocessor.prepare(uploaded_file)
        
        preview_text = PDFTextFormatter.format(
            paper.text
        )

        st.subheader("Paper Information")
        st.write(f"**Title:** {paper.title}")
        st.write(f"**Filename:** {paper.filename}")
        
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Pages", paper.total_pages)

        with col2:
            st.metric("Characters", paper.total_characters)


        PREVIEW_LENGTH = 5000

        st.text_area(
            "Paper Preview",
            value=preview_text,
            height=500,
            disabled=True,
        )

        if len(paper.text) > PREVIEW_LENGTH:
            with st.expander("View Full Paper"):
                st.text_area(
                    "Full Text",
                    value=preview_text,
                    height=800,
                    disabled=True,
                )
       

    except Exception as ex:
        st.error(str(ex))
        return
        
      
    
    
    if st.button(
        "🚀 Analyze Paper",
        type="primary",
        use_container_width=True,
    ):
        uploaded_file.seek(0)
        
        service = AnalysisService()

        try:
            with st.spinner("Analyzing research paper..."):

                record = service.analyze(uploaded_file)

            st.success("Analysis completed successfully.")

            st.divider()

            st.subheader("Paper Information")

            st.write(f"**Title:** {record.title}")
            st.write(f"**Filename:** {record.filename}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Pages", record.total_pages)
                st.metric("Characters", record.total_characters)

            with col2:
                st.metric("Provider", record.provider)
                st.metric("Model", record.model)
                st.metric(
                    "Execution Time",
                    f"{record.execution_time:.2f} sec",
                )

            st.divider()

            st.subheader("AI Analysis")

            st.markdown(record.analysis)

            # Will be used by History and Report pages
            st.session_state["analysis_record"] = record

        except Exception as ex:
            st.error(f"Analysis failed.\n\n{ex}")