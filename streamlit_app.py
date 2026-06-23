import streamlit as st
from app.pdf_reader.pdf_extractor import extract_text_from_pdf

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Research Assistant")
st.subheader("Research Paper Analyzer")

uploaded_file = st.file_uploader(
    "Upload a Research Paper (PDF)",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Reading PDF..."):

        paper_text = extract_text_from_pdf(uploaded_file)

    st.success("PDF Loaded Successfully")

    st.subheader("Extracted Text Preview")

    st.text_area(
        "Paper Content",
        paper_text[:5000],
        height=400
    )

    st.subheader("Summary")

    st.info(
        "Summary module will be integrated in Phase 2."
    )