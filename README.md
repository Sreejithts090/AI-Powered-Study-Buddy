# 🎓 AI Study Buddy

An AI-powered study assistant built with **Python + Streamlit + Google Gemini API** (free tier).

## Features
| Module | What it does |
|---|---|
| 📖 Concept Explainer | Explains any topic at Beginner / Intermediate / Advanced level |
| 📝 Notes Summarizer | Summarizes pasted notes into structured bullet points or paragraphs |
| 🧠 Quiz Generator | Generates MCQ quizzes from a topic or your own notes, with scoring |

---

## Setup Instructions

### 1. Get a free Gemini API Key
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API Key"**
4. Copy the key (starts with `AIza...`)

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Use the app
- Paste your API key in the sidebar
- Choose a tool (Concept Explainer / Notes Summarizer / Quiz Generator)
- Start studying!

---

## Tech Stack
- **Frontend:** Streamlit (Python)
- **AI Model:** Google Gemini 2.5 Flash (free tier — 1,500 requests/day)
- **Libraries:** `google-generativeai`, `streamlit`

## Free Tier Limits
- ✅ 1,500 requests/day
- ✅ No credit card needed
- ✅ No expiry

---

## Project Structure
```
study_buddy/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

*Built for the Edunet Foundation AI Internship Program*
