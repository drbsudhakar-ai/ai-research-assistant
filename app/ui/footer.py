"""
Footer UI for the application.
"""

import streamlit as st

from app.config.branding import get_brand_config
from app.ui.html_renderer import render_html


def render_footer():
    brand = get_brand_config()
    st.divider()
    render_html(f"""
<div class="footer">
<b>{brand.application_name}</b><br>
Version {brand.version}<br>
{brand.credit}<br>
Powered by Streamlit • Ollama • Python
</div>
""")
