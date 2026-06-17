"""
pages_logic/explainer_page.py
───────────────────────────────
Concept Explainer page. Frontend renders inputs and calls the
gemini_service backend function — no API logic lives here.
"""

import streamlit as st
import ui_components as ui
import gemini_service as service


def render(api_key: str):
    ui.section_header(
        "Explainer", "accent",
        "📖 Concept Explainer",
        "Enter any topic and get a clear explanation tailored to your level.",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input(
            "Topic or concept",
            placeholder="e.g. Photosynthesis, Newton's Laws, Recursion in programming...",
        )
    with col2:
        level = st.selectbox("Difficulty level", ["Beginner (ELI5)", "Intermediate", "Advanced / Technical"])

    include_example = st.checkbox("Include a real-world example", value=True)
    include_analogy = st.checkbox("Include an analogy", value=True)

    if st.button("✨ Explain it to me"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Thinking..."):
                result = service.explain_concept(topic, level, include_example, include_analogy, api_key)

            ui.result_card_open(topic, level.split()[0], "accent")
            st.markdown(result)
            ui.card_close()
