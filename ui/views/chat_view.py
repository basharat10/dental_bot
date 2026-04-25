import panel as pn
import re
import json
from core.gemini_helper import gemini_chat
from core.database import save_appointment
from core.booking_parser import normalize_appointment_payload
from core.faq import get_faq_answer
from core.logger import logger

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except (json.JSONDecodeError, TypeError):
            return None
    return None


MAX_CHAT_HISTORY = 20  # Keep last N messages to avoid unbounded token growth


class ChatView:
    def __init__(self):
        self.chat_history = []
        # Professional Header
        header = pn.Column(
            pn.pane.Markdown("## AI Dental Assistant"),
            pn.pane.Markdown(
                "Describe symptoms, ask billing questions, or share an image for guidance.",
                styles={'color': '#475569', 'font-size': '14px'}
            ),
            sizing_mode="stretch_width"
        )

        # Chat History
        self.chat_area = pn.Column(
            scroll=True, 
            height=500, 
            sizing_mode="stretch_width",
            css_classes=['chat-area']
        )
        
        # Initial Bot Message
        self.chat_area.append(
            pn.Column(
                pn.pane.HTML("BRIGHTSMILE AI", css_classes=['msg-label']),
                pn.pane.Markdown(
                    "Hello, I am your virtual dental assistant. How can I support you today?",
                    css_classes=['bot-msg']
                )
            )
        )

        # Chips Section
        self.chips = pn.Row(
            pn.widgets.Button(name="Book cleaning", css_classes=['quick-chip']),
            pn.widgets.Button(name="Clinic hours", css_classes=['quick-chip']),
            pn.widgets.Button(name="Emergency support", css_classes=['quick-chip']),
            pn.widgets.Button(name="Clinic location", css_classes=['quick-chip']),
            styles={'justify-content': 'center', 'margin': '10px 0'}
        )
        
        for chip in self.chips:
            chip.on_click(self.handle_chip)

        # Input Wrapper (Sleek Style)
        self.image_input = pn.widgets.FileInput(accept='.jpg,.jpeg,.png', width=50, css_classes=['icon-btn'], align="center")
        self.input_widget = pn.widgets.TextInput(
            placeholder="Type your message...", 
            sizing_mode="stretch_width",
            styles={'background': 'transparent', 'border': 'none'}
        )
        self.send_button = pn.widgets.Button(name="Send", width=80, height=40, button_type="primary", align="center")
        self.send_button.on_click(self.handle_send)
        
        input_row = pn.Row(
            self.image_input,
            self.input_widget,
            self.send_button,
            css_classes=['input-wrapper'],
            sizing_mode="stretch_width"
        )
        
        disclaimer = pn.pane.Markdown(
            "This assistant provides informational support and does not replace an in-clinic examination.",
            styles={'font-size': '11px', 'color': '#64748b', 'text-align': 'center', 'margin-top': '16px'}
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
        
        # User Message Bubble
        user_content = [pn.pane.Markdown(user_msg)] if user_msg else []
        if image_data:
            user_content.append(pn.pane.JPG(image_data, width=220))
            
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
        
        # Thinking Indicator
        thinking = pn.Column(
            pn.pane.HTML("BRIGHTSMILE AI", css_classes=['msg-label']),
            pn.pane.Markdown("_Typing..._", css_classes=['bot-msg']),
            sizing_mode="stretch_width"
        )
        self.chat_area.append(thinking)
        
        try:
            reply = get_faq_answer(user_msg) if not image_data else None
            if not reply:
                reply = gemini_chat(
                    user_msg or "Analyze photo.",
                    chat_history=self.chat_history,
                    image_data=image_data,
                )

            # Cap chat history to prevent unbounded token growth
            if len(self.chat_history) > MAX_CHAT_HISTORY:
                self.chat_history = self.chat_history[-MAX_CHAT_HISTORY:]

            appointment_data = normalize_appointment_payload(extract_json(reply))
            if appointment_data:
                saved = save_appointment(appointment_data)
                if not saved:
                    logger.warning("Detected booking JSON but failed to save appointment.")

            self.chat_area.remove(thinking)
            
            # Bot Message Bubble
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
            self.chat_area.append(pn.pane.Markdown(f"⚠️ **Error:** {str(e)}", css_classes=['bot-msg']))

    def get_layout(self):
        return self.layout
