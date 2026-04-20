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
        # Chat History Area
        self.chat_area = pn.Column(
            scroll=True, 
            height=500, 
            sizing_mode="stretch_width",
            css_classes=['chat-area']
        )
        
        # Welcome Intro
        intro = pn.pane.Markdown("""
        # 🦷 Welcome to BrightSmile
        How can we help your smile today? Feel free to ask about our services, booking, or dental advice.
        """, css_classes=['bot-msg'], styles={'max-width': '100%'})
        self.chat_area.append(intro)

        # Quick Actions
        self.chips = pn.Row(
            pn.widgets.Button(name="🗓️ Book Cleaning", button_type="light", css_classes=['quick-chip']),
            pn.widgets.Button(name="🕒 Hours", button_type="light", css_classes=['quick-chip']),
            pn.widgets.Button(name="📍 Location", button_type="light", css_classes=['quick-chip']),
            pn.widgets.Button(name="🚨 Emergency", button_type="light", css_classes=['quick-chip']),
        )
        
        for chip in self.chips:
            chip.on_click(self.handle_chip)

        # Input Area
        self.input_widget = pn.widgets.TextInput(
            placeholder="Ask about procedures, pricing, or booking...", 
            sizing_mode="stretch_width"
        )
        self.send_button = pn.widgets.Button(name="Send", button_type="primary", width=100)
        self.send_button.on_click(self.handle_send)
        
        self.layout = pn.Column(
            self.chat_area,
            self.chips,
            pn.Row(self.input_widget, self.send_button, css_classes=['input-area']),
            css_classes=['chat-container']
        )

    def handle_chip(self, event):
        # Extract keywords from chip name
        query = event.obj.name.split(" ", 1)[-1]
        self.input_widget.value = query
        self.handle_send(None)

    def handle_send(self, event):
        user_msg = self.input_widget.value.strip()
        if not user_msg:
            return
        
        self.input_widget.value = ""
        
        # Add User Bubble
        self.chat_area.append(
            pn.Row(
                pn.pane.HTML("<b>You</b>", styles={'font-size': '12px', 'margin-bottom': '5px', 'color': '#718096'}),
                pn.pane.Markdown(user_msg, css_classes=['user-msg']),
                align="end",
                width_policy="max"
            )
        )
        
        # Add Animated Thinking Indicator
        thinking_html = """
        <div class="bot-msg">
            <span style="font-size: 12px; color: #718096; display: block; margin-bottom: 5px;"><b>BrightSmile Bot</b></span>
            <div class="typing-dots">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
        """
        thinking = pn.pane.HTML(thinking_html)
        self.chat_area.append(thinking)
        
        # Logic
        try:
            # 1. FAQ Check
            faq_reply = get_faq_answer(user_msg)
            if faq_reply:
                reply = faq_reply
            else:
                # 2. AI Chat
                reply = gemini_chat(user_msg)

            # Check for booking confirmation
            booking_data = extract_json(reply)
            if booking_data and booking_data.get("status") == "confirmed":
                success = save_appointment(booking_data.get("data", {}))
                if success:
                    reply = re.sub(r'\{.*\}', '✅ **Appointment saved! We look forward to seeing you.**', reply, flags=re.DOTALL)
                else:
                    reply = re.sub(r'\{.*\}', '🚨 **Error saving appointment. Please contact the clinic.**', reply, flags=re.DOTALL)

            # Update thinking with real reply
            self.chat_area.remove(thinking)
            bot_bubble = pn.Column(
                pn.pane.HTML("<b>BrightSmile Bot</b>", styles={'font-size': '12px', 'margin-bottom': '5px', 'color': '#718096'}),
                pn.pane.Markdown(reply),
                css_classes=['bot-msg']
            )
            self.chat_area.append(bot_bubble)
            
        except Exception as e:
            logger.error(f"Chat Error: {e}")
            self.chat_area.remove(thinking)
            error_bubble = pn.Column(
                pn.pane.Markdown(f"🚨 **System Error:** {str(e)}"),
                css_classes=['bot-msg']
            )
            self.chat_area.append(error_bubble)

    def get_layout(self):
        return self.layout
