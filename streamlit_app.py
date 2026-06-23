import streamlit as st
import fitz  # PyMuPDF

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

def extract_text_from_pdf(pdf_file):
    text = ""

    pdf_document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in pdf_document:
        text += page.get_text()

    return text

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