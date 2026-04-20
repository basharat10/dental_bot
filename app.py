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

# Charming Nav Bar
nav_bar = pn.Row(
    pn.pane.HTML(f"<h2 style='margin:0; font-family: \"Playfair Display\", serif;'>🦷 {CLINIC_NAME}</h2>"),
    pn.Spacer(),
    pn.widgets.Button(name="Patient Care", button_type="light", on_click=show_chat),
    pn.widgets.Button(name="Staff Access", button_type="light", on_click=show_admin),
    css_classes=['header-bar'],
    sizing_mode="stretch_width",
    styles={'padding': '30px 10%'}
)

# Patient Auth Flow (Charming Hero)
auth_input = pn.widgets.PasswordInput(name="Portal Code", placeholder="SMILE2025")
auth_button = pn.widgets.Button(name="Enter Boutique Portal", button_type="primary", sizing_mode="stretch_width")
auth_error = pn.pane.Markdown("", styles={'color': '#e53e3e'})

def login_check(event):
    if auth_input.value == ACCESS_CODE:
        show_chat()
    else:
        auth_error.object = "Invalid Access Code."

auth_button.on_click(login_check)

auth_area = pn.Column(
    pn.pane.Markdown(f"""
    # *Experience the Future of Dentistry*
    Welcome to **{CLINIC_NAME}**. Please enter your private invitation code to begin your personalized consultation.
    """),
    auth_input, auth_button, auth_error,
    css_classes=['chat-container'],
    styles={'max-width': '600px', 'margin': '80px auto', 'text-align': 'center'}
)

main_area.append(auth_area)

app_layout = pn.Column(
    nav_bar,
    main_area,
    sizing_mode="stretch_width"
)

if __name__ == "__main__":
    logger.info("Starting Boutique BrightSmile Portal...")
    pn.serve(app_layout, title=CLINIC_NAME)
