# 🎓 AI Study Buddy

An AI-powered study assistant built with **Python + Streamlit + Google Gemini API** (free tier).

Now organized into a clean, modular structure — **backend (AI logic) and frontend (UI) are fully separated.**

## Features
| Module | What it does |
|---|---|
| 📖 Concept Explainer | Explains any topic at Beginner / Intermediate / Advanced level |
| 📝 Notes Summarizer | Summarizes pasted notes into structured bullet points or paragraphs |
| 🧠 Quiz Generator | Generates MCQ quizzes from a topic or your own notes, with scoring |

---

## 📁 Project Structure

```
study_buddy/
├── app.py                  # Entry point — thin router only, no business logic
├── config.py               # Loads settings + API key from .env
├── gemini_service.py        # ALL backend/AI logic — every Gemini API call lives here
├── ui_components.py         # ALL frontend styling — CSS + reusable UI pieces
├── pages_logic/
│   ├── home_page.py         # Home page content
│   ├── explainer_page.py    # Concept Explainer page
│   ├── summarizer_page.py   # Notes Summarizer page
│   └── quiz_page.py         # Quiz Generator page
├── requirements.txt
├── .env.example             # Template for your API key
└── README.md
```

### How the separation works
- **`gemini_service.py`** is the only file that imports `google.generativeai` or talks to the Gemini API. If you ever swap AI providers, this is the only file you touch.
- **`ui_components.py`** is the only file with CSS/styling logic. Change the theme here without touching any AI code.
- **`pages_logic/*.py`** are the page "controllers" — they grab user input, call `gemini_service`, and render results using `ui_components`. They never call the API directly and never contain raw CSS.
- **`app.py`** just decides which page to show. That's it.

---

## ⚙️ Setup Instructions

### 1. Get a free Gemini API Key
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API Key"**
4. Copy the key (starts with `AIza...`)

### 2. Add your API key (so you never paste it into the app again)
1. Rename `.env.example` to `.env`
2. Open `.env` and paste your key:
   ```
   GEMINI_API_KEY=AIza...your_actual_key...
   ```
3. Save the file. The app will now load it automatically every time you run it.

> If you skip this step, the app will simply ask for the key in the sidebar instead — both work.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Use the app
- Choose a tool from the sidebar (Concept Explainer / Notes Summarizer / Quiz Generator)
- Start studying!

---

## Tech Stack
- **Frontend:** Streamlit (Python) — fully separated UI layer
- **Backend / AI:** Google Gemini 2.5 Flash (free tier — 1,500 requests/day)
- **Libraries:** `google-generativeai`, `streamlit`, `python-dotenv`

## Free Tier Limits
- ✅ 1,500 requests/day
- ✅ No credit card needed
- ✅ No expiry

---

*Built for the Edunet Foundation AI Internship Program*
