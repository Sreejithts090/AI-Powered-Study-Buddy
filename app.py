"""
app.py
──────
Entry point. Thin router with all 4 pages.
Sidebar uses Streamlit's native hamburger (top-left).
API key is loaded from .env – no manual paste required.
"""

import streamlit as st

from config import APP_TITLE, APP_ICON, GEMINI_API_KEY
import ui_components as ui
import home_page, explainer_page, summarizer_page, quiz_page

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",  # sidebar visible by default
)

ui.inject_global_css()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    ui.sidebar_brand()

    st.markdown(
        "<p style='color:#7b82a8; font-size:0.78rem; font-family:Syne,sans-serif; "
        "font-weight:600; letter-spacing:0.08em; text-transform:uppercase;'>Navigation</p>",
        unsafe_allow_html=True,
    )

    page = st.radio(
        "",
        ["🏠 Home", "📖 Concept Explainer", "📝 Notes Summarizer", "🧠 Quiz Generator"],
        label_visibility="collapsed",
    )

    ui.sidebar_divider()
    ui.sidebar_footer_note()

# ── Routing (all 4 pages) ──────────────────────────────────────
if page == "🏠 Home":
    home_page.render()
elif page == "📖 Concept Explainer":
    explainer_page.render(GEMINI_API_KEY)
elif page == "📝 Notes Summarizer":
    summarizer_page.render(GEMINI_API_KEY)
elif page == "🧠 Quiz Generator":
    quiz_page.render(GEMINI_API_KEY)