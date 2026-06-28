"""
===========================================================
Project      : AI Research Assistant
File         : footer.py
Version      : 0.3.0
Author       : Dr. B. Sudhakar

Description:
Footer UI for the application.
===========================================================
"""

import streamlit as st


def render_footer():
    """
    Display application footer.
    """

    st.divider()

    st.markdown(
        """
<div class="footer">

<b>AI Research Assistant</b><br>

Version 0.3.0<br>

Developed by <b>Dr. B. Sudhakar</b><br>

Powered by Streamlit • Ollama • Python

</div>
""",
        unsafe_allow_html=True,
    )