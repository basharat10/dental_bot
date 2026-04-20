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
1. GREETING: Warm, professional, and boutique.
2. VISION: Analyze clinical photos/x-rays. Provide observations + Mandatory Disclaimer.
3. BILLING & INSURANCE (NEW): 
   - ACT as a Billing Specialist.
   - USE the 'Clinic Pricing & Insurance Guide' in the Knowledge Base.
   - PROVIDE: 'Estimated Total Cost' and 'Estimated Insurance Coverage' (e.g. 100%, 80%, or 50% based on procedure type).
   - CALCULATE the 'Estimated Out-of-Pocket' for the patient.
4. TRIAGE & SENTIMENT: Identify pain/urgency and refer to emergency hotline (555) 000-9999.
5. RAG: Use KB for procedure explanations.
6. BOOKING: Gather Name, Service, Date, Time, and Notes.
7. JSON CONFIRMATION: Output JSON for confirmed bookings.
8. MULTILINGUAL: Respond in user's language.
"""

chat_history = []

def gemini_chat(user_text, image_data=None):
    """Sends user message (and optional image) to Gemini."""
    try:
        logger.info(f"User input: {user_text} (Image: {image_data is not None})")
        
        parts = [types.Part(text=user_text)]
        if image_data:
            parts.append(types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data)))

        chat_history.append(
            types.Content(role="user", parts=parts)
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
