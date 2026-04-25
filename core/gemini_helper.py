from config import GEMINI_API_KEY, GEMINI_MODEL, KNOWLEDGE_BASE_DIR
from core.logger import logger

_CLIENT = None
_TYPES = None
_INIT_ERROR = None


def get_gemini_client_and_types():
    global _CLIENT, _TYPES, _INIT_ERROR
    if _CLIENT is not None and _TYPES is not None:
        return _CLIENT, _TYPES
    if _INIT_ERROR is not None:
        raise RuntimeError("Gemini client unavailable due to earlier initialization error.") from _INIT_ERROR

    try:
        from google import genai
        from google.genai import types

        if GEMINI_API_KEY and GEMINI_API_KEY.startswith("AQ."):
            from google.auth.credentials import Credentials

            class TokenCredentials(Credentials):
                def __init__(self, token):
                    super().__init__()
                    self.token = token

                def apply(self, headers, token=None):
                    headers["Authorization"] = f"Bearer {self.token}"

                def before_request(self, request, method, url, headers):
                    self.apply(headers)

                def refresh(self, request):
                    raise RuntimeError("Token credentials cannot be refreshed automatically.")

            _CLIENT = genai.Client(credentials=TokenCredentials(GEMINI_API_KEY))
        else:
            _CLIENT = genai.Client(api_key=GEMINI_API_KEY)
        _TYPES = types
        return _CLIENT, _TYPES
    except Exception as exc:
        _INIT_ERROR = exc
        logger.error("Failed to initialize Gemini client: %s", exc)
        raise

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

def gemini_chat(user_text, chat_history=None, image_data=None, max_retries=3):
    """Sends user message (and optional image) to Gemini with automatic retry on transient errors."""
    import time

    if chat_history is None:
        chat_history = []

    logger.info(
        "Gemini request received. text_length=%s, has_image=%s, history_length=%s",
        len(user_text or ""),
        image_data is not None,
        len(chat_history),
    )

    client, types = get_gemini_client_and_types()

    parts = [types.Part(text=user_text)]
    if image_data:
        parts.append(types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data)))

    chat_history.append(
        types.Content(role="user", parts=parts)
    )

    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                ),
                contents=chat_history,
            )

            reply = response.text or ""
            logger.info("Gemini response generated. reply_length=%s", len(reply))

            chat_history.append(
                types.Content(role="model", parts=[types.Part(text=reply)])
            )

            return reply
        except Exception as e:
            last_error = e
            error_str = str(e)
            is_retryable = any(code in error_str for code in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))

            if is_retryable and attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                logger.warning(
                    "Gemini transient error (attempt %s/%s), retrying in %ss: %s",
                    attempt + 1, max_retries, wait, e,
                )
                time.sleep(wait)
                continue

            # Non-retryable error or final attempt — roll back the user message
            logger.error("Gemini API Error (attempt %s/%s): %s", attempt + 1, max_retries, e)
            chat_history.pop()  # remove the user message we appended
            raise last_error

