import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key/token from project root .env
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

# REWIRING: If it's an AQ. token, we handle it as an OAuth2 credential
if api_key and api_key.startswith("AQ."):
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

    client = genai.Client(credentials=TokenCredentials(api_key))
else:
    client = genai.Client(api_key=api_key)

# System prompt
SYSTEM_PROMPT = """
You are DentalBot, a friendly assistant for BrightSmile Dental Clinic.

Your tasks:
1. Greet the customer politely.
2. If the user wants to book an appointment:
   - Ask for their Name, Service (e.g., Cleaning, Filling), Date, Time, and any Notes.
   - Once all details are gathered, summarize them and ask for confirmation.
3. If the user CONFIRMS the appointment, you MUST output a JSON block at the end of your message.

JSON Format for confirmation:
{
  "status": "confirmed",
  "data": {
    "name": "...",
    "service": "...",
    "date": "...",
    "time": "...",
    "notes": "..."
  }
}

4. Answer general questions about the clinic.
5. Always ask: "Is there anything else I can help you with?"
"""

# Maintain chat history manually
chat_history = []

def gemini_chat(user_text):
    """
    Sends user message to Gemini and returns reply.
    """
    chat_history.append(
        types.Content(role="user", parts=[types.Part(text=user_text)])
    )

    response = client.models.generate_content(
        model="gemini-flash-latest",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            # We'll use plain text but instruct it to include JSON so we can parse it easily
        ),
        contents=chat_history,
    )

    reply = response.text
    chat_history.append(
        types.Content(role="model", parts=[types.Part(text=reply)])
    )

    return reply
