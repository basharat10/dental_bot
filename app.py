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

# Sleek Navbar
nav_bar = pn.Row(
    pn.pane.Markdown(f"### 🦷 **{CLINIC_NAME}**", styles={'margin': '0', 'color': '#0f172a'}),
    pn.Spacer(),
    pn.widgets.Button(name="Consultation", button_type="light", on_click=show_chat, width=130),
    pn.widgets.Button(name="Staff Access", button_type="light", on_click=show_admin, width=130),
    sizing_mode="stretch_width",
    styles={'padding': '15px 8%', 'background': '#ffffff', 'border-bottom': '1px solid #e2e8f0', 'box-shadow': '0 1px 2px 0 rgba(0,0,0,0.05)'}
)

# Login Hero Screen
auth_input = pn.widgets.PasswordInput(placeholder="Invitation Code", width=300, align="center")
auth_button = pn.widgets.Button(name="Access Secure Portal", button_type="primary", width=300, align="center")
auth_error = pn.pane.Markdown("", styles={'color': '#ef4444'})

def login_check(event):
    if auth_input.value == ACCESS_CODE:
        show_chat()
    else:
        auth_error.object = "Invalid invitation code."

auth_button.on_click(login_check)

auth_area = pn.Column(
    pn.pane.Markdown(f"# Welcome to {CLINIC_NAME}"),
    pn.pane.Markdown("Please enter your private clinic code to begin.", styles={'color': '#64748b'}),
    auth_input, auth_button, auth_error,
    css_classes=['chat-container'],
    styles={'text-align': 'center', 'margin-top': '100px'}
)

main_area.append(auth_area)

app_layout = pn.Column(nav_bar, main_area, sizing_mode="stretch_width")

if __name__ == "__main__":
    logger.info("Launching Sleek BrightSmile Portal...")
    pn.serve(app_layout, title=CLINIC_NAME)
