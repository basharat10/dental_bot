import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL, KNOWLEDGE_BASE_DIR
from core.logger import logger

# Initialize Gemini Client
if GEMINI_API_KEY and GEMINI_API_KEY.startswith("AQ."):
    from google.auth.credentials import Credentials
    class TokenCredentials(Credentials):
        def __init__(self, token):
            super().__init__()
            self.token = token
        def apply(self, headers, token=None):
            headers['Authorization'] = f'Bearer {self.token}'
        def before_request(self, request, method, url, headers):
            self.apply(headers)
        def refresh(self, request):
            pass
    client = genai.Client(credentials=TokenCredentials(GEMINI_API_KEY))
else:
    client = genai.Client(api_key=GEMINI_API_KEY)

def load_knowledge_base():
    """Loads all markdown files from the knowledge base directory."""
    kb_content = ""
    for file in KNOWLEDGE_BASE_DIR.glob("*.md"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                kb_content += f"\n--- {file.name} ---\n" + f.read()
        except Exception as e:
            logger.error(f"Error loading KB file {file}: {e}")
    return kb_content

SYSTEM_PROMPT = f"""
You are DentalBot, a premium AI concierge for BrightSmile Dental Clinic.

KNOWLEDGE BASE:
{load_knowledge_base()}

YOUR CAPABILITIES:
1. Greet patients warmly.
2. TRIAGE & SENTIMENT: If the user mentions "pain", "broken", "bleeding", or "urgent", acknowledge the urgency and advise them to call our emergency hotline (555) 000-9999 immediately while still helping them book.
3. RAG: Use the provided Knowledge Base to explain procedures (Cleaning, Root Canal, etc.) accurately.
4. BOOKING: Gather Name, Service, Date, Time, and Notes.
5. JSON CONFIRMATION: Once an appointment is confirmed by the user, you MUST include this JSON block at the very end:
{{
  "status": "confirmed",
  "data": {{
    "name": "...",
    "service": "...",
    "date": "...",
    "time": "...",
    "notes": "..."
  }}
}}

6. MULTILINGUAL: Respond in the same language the user uses.
"""

chat_history = []

def gemini_chat(user_text):
    """Sends user message to Gemini and returns reply with sentiment awareness."""
    try:
        logger.info(f"User input: {user_text}")
        
        chat_history.append(
            types.Content(role="user", parts=[types.Part(text=user_text)])
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            ),
            contents=chat_history,
        )

        reply = response.text
        logger.info(f"AI Reply: {reply[:100]}...")
        
        chat_history.append(
            types.Content(role="model", parts=[types.Part(text=reply)])
        )

        return reply
    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        raise e
