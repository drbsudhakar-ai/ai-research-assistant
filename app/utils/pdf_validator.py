"""
===============================================================================
Project      : AI Research Assistant
Module       : PDF Validator
File         : pdf_validator.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Utility module for validating uploaded PDF documents.

Responsibilities:
    - Validate uploaded file existence.
    - Validate PDF file extension.
    - Validate MIME type.
    - Validate maximum file size.
    - Validate PDF integrity.

Notes:
    - This module contains no Streamlit UI.
    - Validation failures raise ValueError.
===============================================================================
"""

from __future__ import annotations

from io import BytesIO

import fitz  # PyMuPDF

__all__ = [
    "PDFValidator",
]


class PDFValidator:
    """
    Validate uploaded PDF documents.
    """

    ALLOWED_EXTENSION = ".pdf"
    ALLOWED_MIME_TYPE = "application/pdf"

    # Maximum upload size (20 MB)
    MAX_FILE_SIZE = 20 * 1024 * 1024

    def validate(self, uploaded_file) -> None:
        """
        Validate an uploaded PDF.

        Parameters
        ----------
        uploaded_file
            Streamlit UploadedFile instance.

        Raises
        ------
        ValueError
            If validation fails.
        """

        self._validate_exists(uploaded_file)
        self._validate_extension(uploaded_file.name)
        self._validate_mime_type(uploaded_file.type)
        self._validate_file_size(uploaded_file.size)
        self._validate_pdf_structure(uploaded_file)

    # =========================================================================
    # Private Validation Methods
    # =========================================================================

    @staticmethod
    def _validate_exists(uploaded_file) -> None:
        """
        Ensure a file has been uploaded.
        """

        if uploaded_file is None:
            raise ValueError(
                "Please upload a PDF document."
            )

    def _validate_extension(self, filename: str) -> None:
        """
        Validate file extension.
        """

        if not filename.lower().endswith(
            self.ALLOWED_EXTENSION
        ):
            raise ValueError(
                "Only PDF (.pdf) files are supported."
            )

    def _validate_mime_type(self, mime_type: str) -> None:
        """
        Validate MIME type.
        """

        if mime_type != self.ALLOWED_MIME_TYPE:
            raise ValueError(
                "Invalid PDF MIME type."
            )

    def _validate_file_size(
        self,
        file_size: int,
    ) -> None:
        """
        Validate uploaded file size.
        """

        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(
                "PDF exceeds the maximum allowed size "
                "(20 MB)."
            )

    @staticmethod
    def _validate_pdf_structure(
        uploaded_file,
    ) -> None:
        """
        Validate PDF integrity.

        Attempts to open the document using PyMuPDF.
        """

        try:
            pdf_bytes = uploaded_file.getvalue()

            document = fitz.open(
                stream=BytesIO(pdf_bytes),
                filetype="pdf",
            )

            if document.page_count == 0:
                raise ValueError(
                    "PDF contains no pages."
                )

            document.close()

        except Exception as exc:
            raise ValueError(
                "Invalid or corrupted PDF document."
            ) from exc