import panel as pn
from config import CLINIC_NAME, ACCESS_CODE
from ui.styles import apply_styles
from ui.views.chat_view import ChatView
from ui.views.admin_view import AdminView
from core.logger import logger

# Apply Global Styles
apply_styles()

# Layout State
main_area = pn.Column(sizing_mode="stretch_width")

# Navigation Functions
def show_chat(event=None):
    main_area.clear()
    main_area.append(ChatView().get_layout())

def show_admin(event=None):
    main_area.clear()
    main_area.append(AdminView().get_layout())

# Navbar (Minimalist Gray)
nav_bar = pn.Row(
    pn.pane.Markdown(f"### 🦷 {CLINIC_NAME}", styles={'margin': '0'}),
    pn.Spacer(),
    pn.widgets.Button(name="Consultation", button_type="light", on_click=show_chat, width=120),
    pn.widgets.Button(name="Staff Access", button_type="light", on_click=show_admin, width=120),
    sizing_mode="stretch_width",
    styles={'padding': '15px 5%', 'background': '#ffffff', 'border-bottom': '1px solid #e2e8f0'}
)

# Login Screen (Clean White)
auth_input = pn.widgets.PasswordInput(placeholder="Enter Portal Code", width=250, align="center")
auth_button = pn.widgets.Button(name="Access Portal", button_type="primary", width=250, align="center")
auth_error = pn.pane.Markdown("", styles={'color': '#e53e3e'})

def login_check(event):
    if auth_input.value == ACCESS_CODE:
        show_chat()
    else:
        auth_error.object = "Invalid Code."

auth_button.on_click(login_check)

auth_area = pn.Column(
    pn.pane.Markdown(f"# Welcome to {CLINIC_NAME}"),
    pn.pane.Markdown("Please sign in with your clinic access code.", styles={'color': '#718096'}),
    auth_input, auth_button, auth_error,
    css_classes=['chat-container'],
    styles={'text-align': 'center', 'margin-top': '80px'}
)

main_area.append(auth_area)

app_layout = pn.Column(nav_bar, main_area, sizing_mode="stretch_width")

if __name__ == "__main__":
    logger.info("Launching Minimalist Dental Portal...")
    pn.serve(app_layout, title=CLINIC_NAME)
