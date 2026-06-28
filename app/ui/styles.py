"""
styles.py
------------------------------------
Contains all custom CSS styles used by
the AI Research Assistant.

Author : Dr. B. Sudhakar
Version: 0.3.0
"""

import streamlit as st


def load_css():
    """Load custom CSS for the application."""

    st.markdown(
        """
        <style>

        /* ---------------------------------------------------------
           GLOBAL
        --------------------------------------------------------- */

        .stApp{
            background-color:#F8FAFC;
        }

        html, body, [class*="css"]{
            font-family: "Segoe UI", sans-serif;
            color:#1F2937;
        }


        /* ---------------------------------------------------------
           HERO TITLE
        --------------------------------------------------------- */

        .hero-title{
            font-size:48px;
            font-weight:700;
            color:#1E3A8A;
            margin-bottom:0px;
        }

        .hero-subtitle{
            font-size:22px;
            color:#475569;
            margin-top:5px;
            margin-bottom:20px;
        }


        /* ---------------------------------------------------------
           INFORMATION CARD
        --------------------------------------------------------- */

        .info-card{

            background:white;

            padding:20px;

            border-radius:12px;

            border-left:6px solid #1E3A8A;

            box-shadow:0 2px 10px rgba(0,0,0,0.08);

            margin-bottom:15px;
        }


        /* ---------------------------------------------------------
           SIDEBAR
        --------------------------------------------------------- */

        section[data-testid="stSidebar"]{

            background-color:#FFFFFF;

            border-right:1px solid #E2E8F0;

        }


        /* ---------------------------------------------------------
           BUTTONS
        --------------------------------------------------------- */

        .stButton>button{

            width:100%;

            background:#1E3A8A;

            color:white;

            border-radius:8px;

            border:none;

            font-size:18px;

            font-weight:600;

            padding:12px;

            transition:0.3s;
        }

        .stButton>button:hover{

            background:#2563EB;

            color:white;

        }


        /* ---------------------------------------------------------
           TEXT AREA
        --------------------------------------------------------- */

        textarea{

            border-radius:10px !important;

            border:1px solid #CBD5E1 !important;

        }


        /* ---------------------------------------------------------
           FILE UPLOADER
        --------------------------------------------------------- */

        div[data-testid="stFileUploader"]{

            border:2px dashed #94A3B8;

            border-radius:12px;

            padding:15px;

        }


        /* ---------------------------------------------------------
           SUCCESS MESSAGE
        --------------------------------------------------------- */

        .success-box{

            background:#ECFDF5;

            padding:15px;

            border-left:5px solid #10B981;

            border-radius:10px;

        }


        /* ---------------------------------------------------------
           FOOTER
        --------------------------------------------------------- */

        .footer{

            text-align:center;

            color:#64748B;

            margin-top:50px;

            padding:20px;

            font-size:14px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )