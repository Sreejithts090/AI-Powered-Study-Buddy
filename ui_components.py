"""
ui_components.py
─────────────────
Pure frontend layer: CSS styling + reusable visual components.
Nothing in this file ever calls the Gemini API — it only renders
markup. app.py imports from here to build each page.
"""

import streamlit as st


def inject_global_css():
    """Inject the app's custom dark theme CSS. Call once at the top of app.py."""
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

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header is kept visible so the hamburger shows up */
    .block-container {padding-top: 2rem; max-width: 1100px;}

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

    h1, h2, h3 {font-family: 'Syne', sans-serif;}

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

    .buddy-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
    }
    .buddy-card-accent {border-left: 4px solid var(--accent);}
    .buddy-card-green {border-left: 4px solid var(--accent2);}
    .buddy-card-yellow {border-left: 4px solid var(--accent3);}

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

    .stAlert {border-radius: 10px !important;}
    div[data-testid="stSpinner"] {color: var(--accent) !important;}

    div[data-baseweb="select"] > div {
        background: var(--card2) !important;
        border-color: var(--border) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_brand():
    """Logo/brand block at the top of the sidebar."""
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
        <span style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:800;
                     background: linear-gradient(135deg,#7c6af7,#56cfb2);
                     -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            🎓 Study Buddy
        </span>
    </div>
    <hr style='border-color:#252d4a; margin: 1rem 0;'>
    """, unsafe_allow_html=True)


def sidebar_divider():
    st.markdown("<hr style='border-color:#252d4a; margin:1rem 0;'>", unsafe_allow_html=True)


def sidebar_footer_note():
    st.markdown("""
    <div style='color:#7b82a8; font-size:0.78rem; line-height:1.6;'>
        <b style='color:#e8eaf6;'>
    </div>
    """, unsafe_allow_html=True)


def hero_banner():
    st.markdown("""
    <div class='hero'>
        <h1 style='font-family:Syne,sans-serif; font-size:2.4rem; font-weight:800; margin:0 0 0.5rem 0;
                   background:linear-gradient(135deg,#7c6af7 0%,#56cfb2 100%);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            Your AI-Powered Study Buddy
        </h1>
        <p style='color:#a0a8cc; font-size:1.05rem; max-width:600px; line-height:1.7; margin:0;'>
            Struggling with complex concepts? Need to summarize your notes fast?
            Want a quick quiz to test yourself? Study Buddy has you covered.
        </p>
    </div>
    """, unsafe_allow_html=True)


def feature_card(chip_label, chip_class, title, description):
    st.markdown(f"""
    <div class='buddy-card buddy-card-{chip_class}'>
        <span class='chip {"chip-" + chip_class if chip_class != "accent" else ""}'>{chip_label}</span>
        <h3 style='font-family:Syne,sans-serif; margin:1rem 0 0.5rem 0; font-size:1.15rem;'>{title}</h3>
        <p style='color:#7b82a8; font-size:0.9rem; line-height:1.6; margin:0;'>
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)


def getting_started_card():
    st.markdown("""
    <div class='buddy-card' style='margin-top:1.5rem; background:linear-gradient(135deg,#141828,#1a1535);'>
        <h3 style='font-family:Syne,sans-serif; font-size:1rem; margin:0 0 0.8rem 0; color:#7b82a8;
                   text-transform:uppercase; letter-spacing:0.08em;'>How to get started</h3>
        <div style='display:flex; gap:2rem; flex-wrap:wrap;'>
            <div style='display:flex; align-items:center; gap:0.7rem;'>
                <span style='background:rgba(124,106,247,0.2); color:#7c6af7; width:28px; height:28px;
                             border-radius:50%; display:flex; align-items:center; justify-content:center;
                             font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem;'>1</span>
                <span style='color:#a0a8cc; font-size:0.9rem;'>API key is loaded automatically from .env</span>
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


def section_header(chip_label, chip_class, title, subtitle):
    chip_css = "chip" if chip_class == "accent" else f"chip chip-{chip_class}"
    st.markdown(f"<span class='{chip_css}'>{chip_label}</span>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-family:Syne,sans-serif; margin:0.5rem 0 0.2rem 0;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#7b82a8; margin-bottom:1.5rem;'>{subtitle}</p>", unsafe_allow_html=True)


def result_card_open(title, badge_text, card_class="accent"):
    st.markdown(f"""
    <div class='buddy-card buddy-card-{card_class}' style='margin-top:1rem;'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
            <span style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem;'>{title}</span>
            <span class='chip {"chip-" + card_class if card_class != "accent" else ""}'>{badge_text}</span>
        </div>
    """, unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def score_card(score, total):
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
