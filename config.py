"""
config.py
─────────
Central place for configuration and the Gemini API key.

The key is loaded from a `.env` file (so you only enter it once and
never paste it into the app UI again). If the .env file or key is
missing, the app will fall back to asking for it in the sidebar.
"""

import os

# Try to load environment variables from a local .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed -> will rely on OS env vars only

# ── Settings ──────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

APP_TITLE = "AI Study Buddy"
APP_ICON = "🎓"
