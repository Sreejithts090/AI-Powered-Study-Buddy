import streamlit as st
import google.generativeai as genai
import json
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg: #0d0f1a;
    --card: #141828;
    --card2: #1a2035;
    --accent: #7c6af7;
    --accent2: #56cfb2;
    --accent3: #f7c56a;
    --text: #e8eaf6;
    --muted: #7b82a8;
    --border: #252d4a;
    --radius: 16px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Hide default streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1100px;}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--text);
    padding: 6px 0;
}

/* ── Headings ── */
h1, h2, h3 {font-family: 'Syne', sans-serif;}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #9b8cf9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,106,247,0.4) !important;
}

/* ── Cards ── */
.buddy-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
}
.buddy-card-accent {
    border-left: 4px solid var(--accent);
}
.buddy-card-green {
    border-left: 4px solid var(--accent2);
}
.buddy-card-yellow {
    border-left: 4px solid var(--accent3);
}

/* ── Quiz option buttons ── */
.quiz-option {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    margin: 0.4rem 0;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    width: 100%;
    text-align: left;
}
.quiz-option:hover {background: var(--border);}
.quiz-option.correct {
    background: rgba(86,207,178,0.15);
    border-color: var(--accent2);
    color: var(--accent2);
}
.quiz-option.wrong {
    background: rgba(247,107,107,0.15);
    border-color: #f76b6b;
    color: #f76b6b;
}

/* ── Tag chips ── */
.chip {
    display: inline-block;
    background: rgba(124,106,247,0.15);
    color: var(--accent);
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.78rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-right: 6px;
}
.chip-green {
    background: rgba(86,207,178,0.12);
    color: var(--accent2);
    border-color: rgba(86,207,178,0.3);
}
.chip-yellow {
    background: rgba(247,197,106,0.12);
    color: var(--accent3);
    border-color: rgba(247,197,106,0.3);
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #141828 0%, #1a1040 50%, #0d1f2d 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(124,106,247,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 150px; height: 150px;
    background: radial-gradient(circle, rgba(86,207,178,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

/* ── Streamlit spinner & alerts ── */
.stAlert {border-radius: 10px !important;}
div[data-testid="stSpinner"] {color: var(--accent) !important;}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: var(--card2) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Gemini setup ──────────────────────────────────────────────────────────────
def get_model():
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def call_gemini(prompt: str) -> str:
    model = get_model()
    if model is None:
        return "⚠️ Please enter your Gemini API key in the sidebar first."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
        <span style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:800;
                     background: linear-gradient(135deg,#7c6af7,#56cfb2);
                     -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            🎓 Study Buddy
        </span>
        <p style='color:#7b82a8; font-size:0.8rem; margin:0.2rem 0 0 0;'>Powered by Gemini AI</p>
    </div>
    <hr style='border-color:#252d4a; margin: 1rem 0;'>
    """, unsafe_allow_html=True)

    api_key = st.text_input(
        "🔑 Gemini API Key",
        type="password",
        placeholder="Paste your API key here",
        help="Get your free key at aistudio.google.com",
    )
    if api_key:
        st.session_state["api_key"] = api_key
        st.success("API key saved ✓", icon="✅")

    st.markdown("<hr style='border-color:#252d4a; margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7b82a8; font-size:0.78rem; font-family:Syne,sans-serif; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;'>Navigation</p>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠 Home", "📖 Concept Explainer", "📝 Notes Summarizer", "🧠 Quiz Generator"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#252d4a; margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#7b82a8; font-size:0.78rem; line-height:1.6;'>
        <b style='color:#e8eaf6;'>Free Tier Limits</b><br>
        ✦ 1,500 requests/day<br>
        ✦ No credit card needed<br>
        ✦ Gemini 2.5 Flash model
    </div>
    """, unsafe_allow_html=True)


# ── HOME ──────────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("""
    <div class='hero'>
        <h1 style='font-family:Syne,sans-serif; font-size:2.4rem; font-weight:800; margin:0 0 0.5rem 0;
                   background:linear-gradient(135deg,#7c6af7 0%,#56cfb2 100%);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            Your AI-Powered Study Buddy
        </h1>
        <p style='color:#a0a8cc; font-size:1.05rem; max-width:600px; line-height:1.7; margin:0;'>
            Struggling with complex concepts? Need to summarize your notes fast?
            Want a quick quiz to test yourself? Study Buddy has you covered — 
            powered by Google's Gemini AI, completely free.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='buddy-card buddy-card-accent'>
            <span class='chip'>Explainer</span>
            <h3 style='font-family:Syne,sans-serif; margin:1rem 0 0.5rem 0; font-size:1.15rem;'>📖 Concept Explainer</h3>
            <p style='color:#7b82a8; font-size:0.9rem; line-height:1.6; margin:0;'>
                Type any topic and get a clear, simple explanation. Choose your level — 
                beginner, intermediate, or advanced.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='buddy-card buddy-card-green'>
            <span class='chip chip-green'>Summarizer</span>
            <h3 style='font-family:Syne,sans-serif; margin:1rem 0 0.5rem 0; font-size:1.15rem;'>📝 Notes Summarizer</h3>
            <p style='color:#7b82a8; font-size:0.9rem; line-height:1.6; margin:0;'>
                Paste your lecture notes or textbook content and get a clean, 
                structured summary with key points highlighted.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='buddy-card buddy-card-yellow'>
            <span class='chip chip-yellow'>Quiz</span>
            <h3 style='font-family:Syne,sans-serif; margin:1rem 0 0.5rem 0; font-size:1.15rem;'>🧠 Quiz Generator</h3>
            <p style='color:#7b82a8; font-size:0.9rem; line-height:1.6; margin:0;'>
                Generate MCQ quizzes from any topic or your own notes. 
                Test yourself and track your score instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='buddy-card' style='margin-top:1.5rem; background:linear-gradient(135deg,#141828,#1a1535);'>
        <h3 style='font-family:Syne,sans-serif; font-size:1rem; margin:0 0 0.8rem 0; color:#7b82a8;
                   text-transform:uppercase; letter-spacing:0.08em;'>How to get started</h3>
        <div style='display:flex; gap:2rem; flex-wrap:wrap;'>
            <div style='display:flex; align-items:center; gap:0.7rem;'>
                <span style='background:rgba(124,106,247,0.2); color:#7c6af7; width:28px; height:28px;
                             border-radius:50%; display:flex; align-items:center; justify-content:center;
                             font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem;'>1</span>
                <span style='color:#a0a8cc; font-size:0.9rem;'>Paste your Gemini API key in the sidebar</span>
            </div>
            <div style='display:flex; align-items:center; gap:0.7rem;'>
                <span style='background:rgba(86,207,178,0.2); color:#56cfb2; width:28px; height:28px;
                             border-radius:50%; display:flex; align-items:center; justify-content:center;
                             font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem;'>2</span>
                <span style='color:#a0a8cc; font-size:0.9rem;'>Pick a tool from the sidebar navigation</span>
            </div>
            <div style='display:flex; align-items:center; gap:0.7rem;'>
                <span style='background:rgba(247,197,106,0.2); color:#f7c56a; width:28px; height:28px;
                             border-radius:50%; display:flex; align-items:center; justify-content:center;
                             font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem;'>3</span>
                <span style='color:#a0a8cc; font-size:0.9rem;'>Start studying smarter!</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── CONCEPT EXPLAINER ─────────────────────────────────────────────────────────
elif page == "📖 Concept Explainer":
    st.markdown("<span class='chip'>Explainer</span>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:Syne,sans-serif; margin:0.5rem 0 0.2rem 0;'>📖 Concept Explainer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7b82a8; margin-bottom:1.5rem;'>Enter any topic and get a clear explanation tailored to your level.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Topic or concept", placeholder="e.g. Photosynthesis, Newton's Laws, Recursion in programming...")
    with col2:
        level = st.selectbox("Difficulty level", ["Beginner (ELI5)", "Intermediate", "Advanced / Technical"])

    include_example = st.checkbox("Include a real-world example", value=True)
    include_analogy = st.checkbox("Include an analogy", value=True)

    if st.button("✨ Explain it to me"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            extras = []
            if include_example:
                extras.append("a real-world example")
            if include_analogy:
                extras.append("a simple analogy")

            extra_str = f"Also include {' and '.join(extras)}." if extras else ""

            prompt = f"""You are an expert educator. Explain the concept of "{topic}" at a {level} level.
Structure your response as:
1. **What is it?** – A clear 2-3 sentence definition.
2. **How it works** – Key points in bullet form (4-6 bullets).
3. **Why it matters** – A brief paragraph on real-world importance.
{extra_str}
Keep the language appropriate for the {level} level. Be concise yet thorough."""

            with st.spinner("Thinking..."):
                result = call_gemini(prompt)

            st.markdown(f"""
            <div class='buddy-card buddy-card-accent' style='margin-top:1rem;'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
                    <span style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem;'>{topic}</span>
                    <span class='chip'>{level.split()[0]}</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)


# ── NOTES SUMMARIZER ──────────────────────────────────────────────────────────
elif page == "📝 Notes Summarizer":
    st.markdown("<span class='chip chip-green'>Summarizer</span>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:Syne,sans-serif; margin:0.5rem 0 0.2rem 0;'>📝 Notes Summarizer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7b82a8; margin-bottom:1.5rem;'>Paste your lecture notes or textbook content and get a structured summary.</p>", unsafe_allow_html=True)

    notes = st.text_area(
        "Paste your notes here",
        height=250,
        placeholder="Paste lecture notes, textbook paragraphs, or any study material here...",
    )

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox("Summary style", ["Concise (bullet points)", "Detailed (paragraphs)", "Key terms + definitions"])
    with col2:
        output_extras = st.multiselect("Also generate", ["Flashcard-style Q&A", "Important dates/numbers", "Key people/entities"])

    if st.button("📝 Summarize my notes"):
        if not notes.strip():
            st.warning("Please paste some notes first.")
        elif len(notes.strip()) < 50:
            st.warning("Notes seem too short. Paste more content for a meaningful summary.")
        else:
            extras_str = ""
            if output_extras:
                extras_str = f"\n\nAlso extract: {', '.join(output_extras)}."

            style_map = {
                "Concise (bullet points)": "a concise bullet-point summary with 6-10 key points",
                "Detailed (paragraphs)": "a detailed paragraph summary covering all major topics",
                "Key terms + definitions": "a list of key terms with their definitions",
            }

            prompt = f"""You are a study assistant. Summarize the following notes as {style_map[summary_style]}.

Structure your response:
1. **📌 Topic Overview** – What subject/topic are these notes about? (1-2 sentences)
2. **🔑 Summary** – The main summary in the chosen style.
3. **⭐ Most Important Point** – The single most critical takeaway.
{extras_str}

Notes to summarize:
---
{notes}
---"""

            with st.spinner("Summarizing..."):
                result = call_gemini(prompt)

            st.markdown(f"""
            <div class='buddy-card buddy-card-green' style='margin-top:1rem;'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
                    <span style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem;'>Summary</span>
                    <span class='chip chip-green'>{summary_style.split("(")[0].strip()}</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)


# ── QUIZ GENERATOR ────────────────────────────────────────────────────────────
elif page == "🧠 Quiz Generator":
    st.markdown("<span class='chip chip-yellow'>Quiz</span>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:Syne,sans-serif; margin:0.5rem 0 0.2rem 0;'>🧠 Quiz Generator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7b82a8; margin-bottom:1.5rem;'>Generate MCQ quizzes from any topic or your own notes. Test yourself instantly.</p>", unsafe_allow_html=True)

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
            source_desc = f"the topic: {quiz_input}" if quiz_source == "A topic/subject" else f"these notes:\n{quiz_input}"

            prompt = f"""Generate {num_q} multiple choice questions (MCQs) about {source_desc}.
Difficulty: {difficulty}

Return ONLY a valid JSON array. No extra text, no markdown fences.
Format:
[
  {{
    "question": "Question text here?",
    "options": ["A) Option1", "B) Option2", "C) Option3", "D) Option4"],
    "answer": "A) Option1",
    "explanation": "Brief explanation of why this is correct."
  }}
]"""

            with st.spinner("Generating quiz..."):
                raw = call_gemini(prompt)

            # Parse JSON
            try:
                clean = re.sub(r"```(?:json)?|```", "", raw).strip()
                questions = json.loads(clean)

                # Store in session state
                st.session_state["quiz"] = questions
                st.session_state["quiz_answers"] = {}
                st.session_state["quiz_submitted"] = False
                st.session_state["score"] = 0

            except Exception:
                st.error("Could not parse quiz. Please try again.")
                st.code(raw)

    # ── Render quiz ──
    if "quiz" in st.session_state and st.session_state["quiz"]:
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
                    st.markdown(f"<p style='color:#56cfb2; font-size:0.88rem;'>✅ Correct!</p>", unsafe_allow_html=True)
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
                score = st.session_state["score"]
                total = len(questions)
                pct = int(score / total * 100)
                color = "#56cfb2" if pct >= 70 else "#f7c56a" if pct >= 40 else "#f76b6b"
                emoji = "🏆" if pct >= 70 else "📚" if pct >= 40 else "💪"

                st.markdown(f"""
                <div class='buddy-card' style='text-align:center; border-color:{color};'>
                    <p style='font-size:2rem; margin:0;'>{emoji}</p>
                    <p style='font-family:Syne,sans-serif; font-size:1.8rem; font-weight:800;
                               color:{color}; margin:0.2rem 0;'>{score}/{total}</p>
                    <p style='color:#7b82a8; font-size:0.9rem; margin:0;'>{pct}% Score</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🔄 Try Again"):
                    del st.session_state["quiz"]
                    del st.session_state["quiz_answers"]
                    st.session_state["quiz_submitted"] = False
                    st.rerun()
