import os
from pathlib import Path
from dotenv import load_dotenv

# Project Paths
BASE_DIR = Path(__file__).resolve().parent
CORE_DIR = BASE_DIR / "core"
DATA_DIR = BASE_DIR / "data"
UI_DIR = BASE_DIR / "ui"
KNOWLEDGE_BASE_DIR = CORE_DIR / "knowledge_base"

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")


def _require_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

# API Configuration
GEMINI_API_KEY = _require_env("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

# Clinic Configuration
CLINIC_NAME = "BrightSmile Dental Clinic"
ACCESS_CODE = _require_env("ACCESS_CODE")
ADMIN_PASSWORD = _require_env("ADMIN_PASSWORD")
ALLOWED_WEBSOCKET_ORIGIN = _require_env("ALLOWED_WEBSOCKET_ORIGIN")
ADMIN_SESSION_TIMEOUT_MINUTES = int(os.getenv("ADMIN_SESSION_TIMEOUT_MINUTES", "15"))

# UI Constants
THEME_COLOR = "#008080"  # Teal
ACCENT_COLOR = "#00bfa5" # Light Teal
BG_COLOR = "#f0f4f8"
