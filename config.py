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

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-flash-latest"

# Clinic Configuration
CLINIC_NAME = "BrightSmile Dental Clinic"
ACCESS_CODE = "SMILE2025"
ADMIN_PASSWORD = "ADMIN_SMILE_2025"

# UI Constants
THEME_COLOR = "#008080"  # Teal
ACCENT_COLOR = "#00bfa5" # Light Teal
BG_COLOR = "#f0f4f8"
