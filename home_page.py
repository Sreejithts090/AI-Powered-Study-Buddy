"""
pages_logic/home_page.py
─────────────────────────
Renders the Home page. Pure frontend - uses ui_components only.
"""

import streamlit as st
import ui_components as ui


def render():
    ui.hero_banner()

    col1, col2, col3 = st.columns(3)

    with col1:
        ui.feature_card(
            "Explainer", "accent",
            "📖 Concept Explainer",
            "Type any topic and get a clear, simple explanation. Choose your level — "
            "beginner, intermediate, or advanced.",
        )
    with col2:
        ui.feature_card(
            "Summarizer", "green",
            "📝 Notes Summarizer",
            "Paste your lecture notes or textbook content and get a clean, "
            "structured summary with key points highlighted.",
        )
    with col3:
        ui.feature_card(
            "Quiz", "yellow",
            "🧠 Quiz Generator",
            "Generate MCQ quizzes from any topic or your own notes. "
            "Test yourself and track your score instantly.",
        )

    ui.getting_started_card()
