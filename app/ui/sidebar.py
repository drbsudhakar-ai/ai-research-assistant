"""
sidebar.py
------------------------------
Sidebar UI for AI Research Assistant

Author : Dr. B. Sudhakar
Version : 0.4.0
"""

import streamlit as st


# ==========================================================
# NAVIGATION
# ==========================================================



def render_sidebar():

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "📜 Analysis History",
        ]
    )

    st.sidebar.divider()
    
    with st.sidebar:

        st.markdown("## 🧠 AI Research Assistant")

        st.divider()

        
        st.markdown("### 🚀 Modules")

        st.checkbox("Paper Analyzer", value=True, disabled=True)
        st.checkbox("Literature Review", disabled=True)
        st.checkbox("Citation Generator", disabled=True)
        st.checkbox("Research Gap Finder", disabled=True)
        st.checkbox("PDF Chat", disabled=True)
        st.checkbox("RAG Search", disabled=True)

        st.divider()

        st.markdown("### 📊 Project Progress")

        st.progress(0.30)

        st.caption("Version 0.3 Development")

        st.divider()
        st.markdown("### 📌 Project Information")

        st.write("**Version** : 0.4.0")
        st.write("**Provider** : Ollama")
        st.write("**Model** : qwen3:4b")
        st.write("**Status** : 🟢 Ready")

        st.divider()

        st.markdown("### 👨‍💻 Developer")

        st.success("Dr. B. Sudhakar")

        st.caption(
            "Building open-source AI tools for Education and Research."
        )
    return page

