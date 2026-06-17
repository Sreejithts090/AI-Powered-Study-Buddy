"""
pages_logic/quiz_page.py
───────────────────────────
Quiz Generator page. Frontend renders the quiz UI and scoring;
all AI generation/parsing happens in gemini_service.generate_quiz().
"""

import streamlit as st
import ui_components as ui
import gemini_service as service


def render(api_key: str):
    ui.section_header(
        "Quiz", "yellow",
        "🧠 Quiz Generator",
        "Generate MCQ quizzes from any topic or your own notes. Test yourself instantly.",
    )

    quiz_source = st.radio("Generate quiz from:", ["A topic/subject", "My own notes"], horizontal=True)

    if quiz_source == "A topic/subject":
        quiz_input = st.text_input("Topic", placeholder="e.g. World War II, Photosynthesis, Python programming...")
    else:
        quiz_input = st.text_area("Paste your notes", height=180, placeholder="Paste notes here to generate questions from them...")

    col1, col2 = st.columns(2)
    with col1:
        num_q = st.slider("Number of questions", 3, 10, 5)
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])

    if st.button("🎯 Generate Quiz"):
        if not quiz_input.strip():
            st.warning("Please enter a topic or paste some notes.")
        else:
            is_topic = quiz_source == "A topic/subject"
            with st.spinner("Generating quiz..."):
                questions, raw_error = service.generate_quiz(quiz_input, is_topic, num_q, difficulty, api_key)

            if questions:
                st.session_state["quiz"] = questions
                st.session_state["quiz_answers"] = {}
                st.session_state["quiz_submitted"] = False
                st.session_state["score"] = 0
            else:
                st.error("Could not parse quiz. Please try again.")
                st.code(raw_error)

    _render_quiz_if_present()


def _render_quiz_if_present():
    if "quiz" not in st.session_state or not st.session_state["quiz"]:
        return

    questions = st.session_state["quiz"]
    submitted = st.session_state.get("quiz_submitted", False)

    st.markdown("<hr style='border-color:#252d4a; margin:1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-family:Syne,sans-serif;'>📋 Your Quiz — {len(questions)} Questions</h3>", unsafe_allow_html=True)

    for i, q in enumerate(questions):
        st.markdown(f"""
        <div class='buddy-card' style='margin-bottom:1rem;'>
            <p style='font-weight:600; margin:0 0 0.8rem 0; font-size:0.95rem;'>
                <span style='color:#7c6af7; font-family:Syne,sans-serif;'>Q{i+1}.</span> {q['question']}
            </p>
        """, unsafe_allow_html=True)

        key = f"q_{i}"
        selected = st.radio(
            f"q{i}",
            q["options"],
            key=key,
            label_visibility="collapsed",
            index=None,
        )
        if selected:
            st.session_state["quiz_answers"][i] = selected

        if submitted:
            user_ans = st.session_state["quiz_answers"].get(i)
            correct = q["answer"]
            if user_ans == correct:
                st.markdown("<p style='color:#56cfb2; font-size:0.88rem;'>✅ Correct!</p>", unsafe_allow_html=True)
            elif user_ans:
                st.markdown(f"<p style='color:#f76b6b; font-size:0.88rem;'>❌ Wrong. Correct answer: <b>{correct}</b></p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color:#f7c56a; font-size:0.88rem;'>⚠️ Not answered. Correct: <b>{correct}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#7b82a8; font-size:0.85rem; font-style:italic;'>💡 {q['explanation']}</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if not submitted:
            if st.button("✅ Submit Quiz"):
                score = sum(
                    1 for i, q in enumerate(questions)
                    if st.session_state["quiz_answers"].get(i) == q["answer"]
                )
                st.session_state["quiz_submitted"] = True
                st.session_state["score"] = score
                st.rerun()
        else:
            ui.score_card(st.session_state["score"], len(questions))

            if st.button("🔄 Try Again"):
                del st.session_state["quiz"]
                del st.session_state["quiz_answers"]
                st.session_state["quiz_submitted"] = False
                st.rerun()
