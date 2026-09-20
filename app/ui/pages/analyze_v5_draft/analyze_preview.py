"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze PDF Preview
File         : analyze_preview.py

Description:
    Displays uploaded research paper PDF inside Analyze page.

Responsibilities:
    - Convert PDF to browser embeddable format
    - Render PDF preview
    - Hide default PDF controls where supported

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import BinaryIO

import streamlit as st



# =============================================================================
# PDF Encoding
# =============================================================================


def _encode_pdf(
    pdf_path: Path,
) -> str:
    """
    Convert PDF file into base64 string.

    Args:
        pdf_path:
            PDF file location.

    Returns:
        Base64 encoded PDF.
    """

    with open(
        pdf_path,
        "rb",
    ) as pdf_file:

        return base64.b64encode(
            pdf_file.read()
        ).decode(
            "utf-8"
        )



# =============================================================================
# Preview Renderer
# =============================================================================


def render_pdf_preview(
    pdf_path: Path | None,
    height: int = 900,
) -> None:
    """
    Render PDF preview.

    Args:
        pdf_path:
            PDF file path.

        height:
            Preview height.
    """

    if pdf_path is None:

        st.info(
            "Upload a PDF to preview the paper."
        )

        return



    if not pdf_path.exists():

        st.error(
            "PDF file not found."
        )

        return



    try:

        pdf_base64 = _encode_pdf(
            pdf_path
        )

        pdf_html = f"""
        <object
            data="data:application/pdf;base64,{pdf_base64}"
            type="application/pdf"
            width="100%"
            height="{height}px">

            <p>
                PDF preview is not supported by this browser.
            </p>

        </object>
        """


        st.markdown(
            pdf_html,
            unsafe_allow_html=True,
        )
        # st.components.v1.html(
        #     pdf_html,
        #     height=height,
        #     scrolling=True,
        # )


    except Exception as exc:

        st.error(
            f"Unable to display PDF preview: {exc}"
        )



# =============================================================================
# Uploaded File Helper
# =============================================================================


def save_uploaded_pdf(
    uploaded_file,
    destination: Path,
) -> Path:
    """
    Save Streamlit uploaded file.

    Args:
        uploaded_file:
            UploadedFile object.

        destination:
            Target path.

    Returns:
        Saved PDF path.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    with open(
        destination,
        "wb",
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    return destination