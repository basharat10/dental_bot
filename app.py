import json
import re
import panel as pn
from core.gemini_helper import gemini_chat
from core.database import save_appointment
from core.faq import get_faq_answer

# Use modern design extensions
pn.extension(raw_css=[
    """
    body { 
        background-color: #f0f4f8; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        padding: 20px;
        max-width: 800px;
        margin: auto;
    }
    .user-msg {
        background-color: #008080;
        color: white;
        border-radius: 15px 15px 0 15px;
        padding: 12px 18px;
        margin-bottom: 15px;
        align-self: flex-end;
        box-shadow: 0 4px 10px rgba(0, 128, 128, 0.2);
    }
    .bot-msg {
        background-color: white;
        color: #333;
        border-radius: 15px 15px 15px 0;
        padding: 12px 18px;
        margin-bottom: 15px;
        border: 1px solid #eef2f7;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    .header-bar {
        background: linear-gradient(90deg, #008080 0%, #00bfa5 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .input-area {
        border-top: 1px solid #eee;
        padding-top: 15px;
    }
    .bk-btn-success {
        background-color: #008080 !important;
        border: none !important;
    }
    """
])

# UI State
panels = []

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: return None
    return None

def collect_messages(_):
    prompt = inp.value.strip()
    if not prompt: return pn.Column(*panels)
    inp.value = ""
    
    print(f"DEBUG: Processing message: {prompt}")

    # 1. Check FAQ
    faq_answer = get_faq_answer(prompt)
    if faq_answer:
        print("DEBUG: FAQ match found")
        reply = faq_answer
    else:
        # 2. Call AI
        print("DEBUG: Calling Gemini AI...")
        try:
            reply = gemini_chat(prompt)
            print("DEBUG: AI replied successfully")
        except Exception as e:
            reply = f"🚨 **AI Engine Error:** {str(e)}"
            print(f"DEBUG: AI Error: {e}")

    # Check for JSON confirmation
    booking_data = extract_json(reply)
    if booking_data and booking_data.get("status") == "confirmed":
        save_appointment(booking_data.get("data", {}))
        display_reply = re.sub(r'\{.*\}', '✅ **Appointment confirmed and added to our system!**', reply, flags=re.DOTALL)
    else:
        display_reply = reply

    # Add messages to UI
    panels.append(pn.Row(pn.pane.Markdown(f"{prompt}", css_classes=['user-msg']), align="end"))
    panels.append(pn.Row(pn.pane.Markdown(f"{display_reply}", css_classes=['bot-msg'])))

    return pn.Column(*panels, scroll=True, height=500)

# Widgets
inp = pn.widgets.TextInput(placeholder="Ask about booking, hours, or services...", disabled=True, sizing_mode="stretch_width")
button = pn.widgets.Button(name="Send", button_type="primary", disabled=True, width=100)

# Auth
auth_input = pn.widgets.PasswordInput(name="Staff/Patient Access Code", placeholder="Enter code (SMILE2025)")
auth_button = pn.widgets.Button(name="Login", button_type="success", sizing_mode="stretch_width")
status_msg = pn.widgets.StaticText(value="🔒 Portal Locked")

def login_check(event):
    if auth_input.value == "SMILE2025":
        inp.disabled = False
        button.disabled = False
        auth_area.visible = False
        status_msg.value = "🟢 **Logged In:** Welcome to BrightSmile Portal"
    else:
        status_msg.value = "🔴 **Access Denied:** Please check your code."

auth_button.on_click(login_check)

# Layout Components
header = pn.Row(
    pn.pane.HTML("<h2>🦷 BrightSmile Portal</h2>"),
    pn.Spacer(),
    status_msg,
    css_classes=['header-bar'],
    sizing_mode="stretch_width"
)

auth_area = pn.Column(
    pn.pane.Markdown("### Welcome Back\nPlease enter your access code to start the secure consultation."),
    auth_input, auth_button,
    styles={'background': 'white', 'padding': '30px', 'border-radius': '15px', 'margin': 'auto', 'max-width': '400px'}
)

chat_area = pn.Column(scroll=True, height=450, sizing_mode="stretch_width")

def send_message(event):
    prompt = inp.value.strip()
    if not prompt: return
    inp.value = ""
    
    # Show User Message
    chat_area.append(pn.Row(pn.pane.Markdown(f"{prompt}", css_classes=['user-msg']), align="end"))
    
    # Show "Thinking..." placeholder
    thinking = pn.pane.Markdown("_DentalBot is thinking..._", css_classes=['bot-msg'])
    chat_area.append(pn.Row(thinking))
    
    # 1. Check FAQ
    faq_answer = get_faq_answer(prompt)
    if faq_answer:
        reply = faq_answer
    else:
        # 2. Call AI
        try:
            reply = gemini_chat(prompt)
        except Exception as e:
            reply = f"🚨 **AI Engine Error:** {str(e)}"

    # Check for JSON confirmation
    booking_data = extract_json(reply)
    if booking_data and booking_data.get("status") == "confirmed":
        save_appointment(booking_data.get("data", {}))
        display_reply = re.sub(r'\{.*\}', '✅ **Appointment confirmed and added to our system!**', reply, flags=re.DOTALL)
    else:
        display_reply = reply

    # Update "Thinking" bubble with real reply
    thinking.object = display_reply

button.on_click(send_message)

# Assemble
app_layout = pn.Column(
    header,
    pn.Column(
        auth_area,
        chat_area,
        pn.Row(inp, button, css_classes=['input-area']),
        css_classes=['chat-container']
    ),
    sizing_mode="stretch_width"
)

if __name__ == "__main__":
    pn.serve(app_layout, title="BrightSmile Dental Clinic")
