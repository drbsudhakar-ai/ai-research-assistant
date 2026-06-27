"""
===============================================================================
Project      : AI Research Assistant
Module       : PDF Utilities
File         : pdf_extractor.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Utility module for extracting text from research paper PDFs.

Responsibilities:
    • Read PDF files
    • Extract text page by page
    • Return extracted text
    • Return PDF statistics

Future Enhancements:
    • OCR support for scanned PDFs
    • Table extraction
    • Figure extraction
    • Citation extraction
===============================================================================
"""

import fitz  # PyMuPDF


class PDFExtractor:
    """
    Utility class for extracting text from PDF documents.
    """

    @staticmethod
    def extract_text(uploaded_file):
        """
        Extract text from an uploaded PDF.

        Parameters
        ----------
        uploaded_file : UploadedFile
            Streamlit uploaded PDF object.

        Returns
        -------
        tuple
            (
                extracted_text,
                total_pages,
                total_characters
            )
        """

        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        extracted_text = ""

        for page in pdf:
            extracted_text += page.get_text()

        total_pages = len(pdf)

        total_characters = len(extracted_text)

        pdf.close()

        return (
            extracted_text,
            total_pages,
            total_characters
        )