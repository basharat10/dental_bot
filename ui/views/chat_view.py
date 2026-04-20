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
            height=600, 
            sizing_mode="stretch_width",
            css_classes=['chat-area']
        )
        
        # Welcome Intro (Redesigned)
        intro = pn.pane.Markdown("""
        # *Welcome to BrightSmile*
        ### Experience Dental Care Redefined.
        How can we help your smile today? 
        """, css_classes=['bot-msg'], styles={'text-align': 'center', 'margin-bottom': '30px'})
        self.chat_area.append(intro)

        # Quick Actions (Charming Chips)
        self.chips = pn.Row(
            pn.widgets.Button(name="🗓️ Book Cleaning", css_classes=['quick-chip']),
            pn.widgets.Button(name="💎 Teeth Whitening", css_classes=['quick-chip']),
            pn.widgets.Button(name="🕒 Clinic Hours", css_classes=['quick-chip']),
            pn.widgets.Button(name="🚨 Emergency", css_classes=['quick-chip']),
            sizing_mode="stretch_width",
            styles={'justify-content': 'center'}
        )
        
        for chip in self.chips:
            chip.on_click(self.handle_chip)

        # Input Area (Floating Style)
        self.image_input = pn.widgets.FileInput(accept='.jpg,.jpeg,.png', sizing_mode="fixed", width=40, height=40)
        self.mic_button = pn.widgets.Button(name="🎤", width=40, height=40, css_classes=['mic-btn'])
        self.input_widget = pn.widgets.TextInput(
            placeholder="Tell us what's on your mind...", 
            sizing_mode="stretch_width"
        )
        self.send_button = pn.widgets.Button(name="Send", button_type="primary", width=100)
        self.send_button.on_click(self.handle_send)
        
        # JS for Speech-to-Text
        self.mic_button.js_on_click(args={'target': self.input_widget}, code="""
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.start();
            target.placeholder = "Listening...";
            recognition.onresult = (event) => {
                target.value = event.results[0][0].transcript;
                target.placeholder = "Ask, upload, or speak...";
            };
        """)

        self.layout = pn.Column(
            self.chat_area,
            self.chips,
            pn.Row(self.image_input, self.mic_button, self.input_widget, self.send_button, css_classes=['input-area']),
            css_classes=['chat-container']
        )

    def handle_chip(self, event):
        query = event.obj.name.split(" ", 1)[-1]
        self.input_widget.value = query
        self.handle_send(None)

    def handle_send(self, event):
        user_msg = self.input_widget.value.strip()
        image_data = self.image_input.value
        
        if not user_msg and not image_data:
            return
        
        self.input_widget.value = ""
        self.image_input.value = None
        
        # Add User Bubble (Right Aligned)
        user_content = [pn.pane.Markdown(user_msg)] if user_msg else []
        if image_data:
            user_content.append(pn.pane.JPG(image_data, width=250))
            
        self.chat_area.append(
            pn.Row(
                pn.Spacer(),
                pn.Column(*user_content, css_classes=['user-msg']),
                sizing_mode="stretch_width"
            )
        )
        
        # Animated Thinking Indicator
        thinking_html = """
        <div class="bot-msg">
            <span style="font-size: 11px; opacity: 0.6; display: block; margin-bottom: 5px;">BRIGHTSMILE BOT</span>
            <div class="typing-dots">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
        """
        thinking = pn.pane.HTML(thinking_html)
        self.chat_area.append(thinking)
        
        try:
            if not image_data:
                faq_reply = get_faq_answer(user_msg)
            else:
                faq_reply = None

            reply = faq_reply or gemini_chat(user_msg or "Analyze photo.", image_data=image_data)

            # Process AI output for cards
            booking_data = extract_json(reply)
            if booking_data and booking_data.get("status") == "confirmed":
                if save_appointment(booking_data.get("data", {})):
                    reply = re.sub(r'\{.*\}', '✨ **Your appointment is perfectly set. See you soon!**', reply, flags=re.DOTALL)

            self.chat_area.remove(thinking)
            
            # Speaker Logic
            speaker_btn = pn.widgets.Button(name="🔊", width=30, height=30, css_classes=['speaker-btn'])
            speaker_btn.js_on_click(args={'text': reply}, code="""
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            """)

            # Dynamic Content
            final_content = []
            
            # Emergency/Triage Card
            if any(x in reply.lower() for x in ["emergency", "hotline", "urgency"]):
                final_content.append(pn.pane.Markdown("🚨 **Urgent Care Protocol Active**", styles={'color': '#e53e3e', 'font-weight': '600'}))

            # Cost Specialist Card
            if "cost" in reply.lower() or "price" in reply.lower():
                final_content.append(pn.Column(pn.pane.Markdown("### 💰 Financial Estimate"), css_classes=['treatment-card']))

            # Main Body
            clean_reply = re.sub(r'\{.*\}', '', reply, flags=re.DOTALL).strip()
            final_content.append(pn.pane.Markdown(clean_reply))

            bot_bubble = pn.Column(
                pn.Row(pn.pane.HTML("<small>BRIGHTSMILE BOT</small>", styles={'opacity': '0.5'}), pn.Spacer(), speaker_btn),
                *final_content,
                css_classes=['bot-msg']
            )
            self.chat_area.append(bot_bubble)
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            self.chat_area.remove(thinking)
            self.chat_area.append(pn.pane.Markdown(f"🙏 **Apologies:** {str(e)}", css_classes=['bot-msg']))

    def get_layout(self):
        return self.layout
