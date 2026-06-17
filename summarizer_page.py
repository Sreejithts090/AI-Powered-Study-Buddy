"""
pages_logic/summarizer_page.py
────────────────────────────────
Notes Summarizer page. Frontend only — calls gemini_service for the AI work.
"""

import streamlit as st
import ui_components as ui
import gemini_service as service


def render(api_key: str):
    ui.section_header(
        "Summarizer", "green",
        "📝 Notes Summarizer",
        "Paste your lecture notes or textbook content and get a structured summary.",
    )

    notes = st.text_area(
        "Paste your notes here",
        height=250,
        placeholder="Paste lecture notes, textbook paragraphs, or any study material here...",
    )

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox(
            "Summary style",
            ["Concise (bullet points)", "Detailed (paragraphs)", "Key terms + definitions"],
        )
    with col2:
        output_extras = st.multiselect(
            "Also generate",
            ["Flashcard-style Q&A", "Important dates/numbers", "Key people/entities"],
        )

    if st.button("📝 Summarize my notes"):
        if not notes.strip():
            st.warning("Please paste some notes first.")
        elif len(notes.strip()) < 50:
            st.warning("Notes seem too short. Paste more content for a meaningful summary.")
        else:
            with st.spinner("Summarizing..."):
                result = service.summarize_notes(notes, summary_style, output_extras, api_key)

            ui.result_card_open("Summary", summary_style.split("(")[0].strip(), "green")
            st.markdown(result)
            ui.card_close()
