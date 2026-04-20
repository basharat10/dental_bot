import panel as pn
import re
import json
from core.gemini_helper import gemini_chat
from core.database import save_appointment
from core.faq import get_faq_answer
from core.logger import logger

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: return None
    return None

class ChatView:
    def __init__(self):
        # Header Info
        header = pn.Column(
            pn.pane.Markdown("# Patient Consultation"),
            pn.pane.Markdown("_Welcome to BrightSmile. How can we assist you today?_", styles={'color': '#718096'}),
            sizing_mode="stretch_width"
        )

        # Chat History Area
        self.chat_area = pn.Column(
            scroll=True, 
            height=450, 
            sizing_mode="stretch_width",
            css_classes=['chat-area']
        )
        
        # Quick Actions
        self.chips = pn.Row(
            pn.widgets.Button(name="🗓️ Book Cleaning", css_classes=['quick-chip']),
            pn.widgets.Button(name="🕒 Hours", css_classes=['quick-chip']),
            pn.widgets.Button(name="🚨 Emergency", css_classes=['quick-chip']),
            sizing_mode="stretch_width",
            styles={'justify-content': 'center'}
        )
        
        for chip in self.chips:
            chip.on_click(self.handle_chip)

        # Input Section (Clean Gemini Layout)
        self.image_input = pn.widgets.FileInput(accept='.jpg,.jpeg,.png', width=50, css_classes=['icon-btn'])
        self.mic_button = pn.widgets.Button(name="🎤", width=40, css_classes=['icon-btn'])
        self.input_widget = pn.widgets.TextInput(
            placeholder="Type your message here...", 
            sizing_mode="stretch_width"
        )
        self.send_button = pn.widgets.Button(name="➤", width=50, height=40, button_type="primary")
        self.send_button.on_click(self.handle_send)
        
        # JS for Speech-to-Text
        self.mic_button.js_on_click(args={'target': self.input_widget}, code="""
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.start();
            recognition.onresult = (event) => {
                target.value = event.results[0][0].transcript;
            };
        """)

        input_row = pn.Row(
            self.image_input,
            self.mic_button,
            self.input_widget,
            self.send_button,
            css_classes=['input-wrapper'],
            sizing_mode="stretch_width"
        )
        
        disclaimer = pn.pane.Markdown(
            "AI Assistant: Professional dental advice should always be sought for clinical diagnosis.",
            css_classes=['footer-text']
        )

        self.layout = pn.Column(
            header,
            self.chat_area,
            self.chips,
            input_row,
            disclaimer,
            css_classes=['chat-container']
        )

    def handle_chip(self, event):
        self.input_widget.value = event.obj.name.split(" ", 1)[-1]
        self.handle_send(None)

    def handle_send(self, event):
        user_msg = self.input_widget.value.strip()
        image_data = self.image_input.value
        
        if not user_msg and not image_data:
            return
        
        self.input_widget.value = ""
        self.image_input.value = None
        
        # Add User Message
        user_content = [pn.pane.Markdown(user_msg)] if user_msg else []
        if image_data:
            user_content.append(pn.pane.JPG(image_data, width=200))
            
        self.chat_area.append(
            pn.Row(
                pn.Spacer(),
                pn.Column(
                    pn.pane.HTML("PATIENT", css_classes=['msg-label'], styles={'text-align': 'right'}),
                    pn.Column(*user_content, css_classes=['user-msg']),
                    sizing_mode="stretch_width"
                ),
                sizing_mode="stretch_width"
            )
        )
        
        # Bot Loading State
        thinking = pn.Column(
            pn.pane.HTML("BRIGHTSMILE AI", css_classes=['msg-label']),
            pn.pane.Markdown("...", css_classes=['bot-msg']),
            sizing_mode="stretch_width"
        )
        self.chat_area.append(thinking)
        
        try:
            reply = get_faq_answer(user_msg) if not image_data else None
            if not reply:
                reply = gemini_chat(user_msg or "Explain photo.", image_data=image_data)

            # JSON Confirmation Logic
            booking_data = extract_json(reply)
            if booking_data and booking_data.get("status") == "confirmed":
                if save_appointment(booking_data.get("data", {})):
                    reply = re.sub(r'\{.*\}', '✅ **Appointment confirmed.**', reply, flags=re.DOTALL)

            self.chat_area.remove(thinking)
            
            # Add Bot Message
            self.chat_area.append(
                pn.Column(
                    pn.pane.HTML("BRIGHTSMILE AI", css_classes=['msg-label']),
                    pn.pane.Markdown(re.sub(r'\{.*\}', '', reply).strip(), css_classes=['bot-msg']),
                    sizing_mode="stretch_width"
                )
            )
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            self.chat_area.remove(thinking)
            self.chat_area.append(pn.pane.Markdown(f"⚠️ Error: {str(e)}", css_classes=['bot-msg']))

    def get_layout(self):
        return self.layout
