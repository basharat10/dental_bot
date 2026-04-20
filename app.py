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

# Professional Nav Bar
nav_bar = pn.Row(
    pn.pane.HTML(f"<h2 style='margin:0;'>🦷 {CLINIC_NAME}</h2>"),
    pn.Spacer(),
    pn.widgets.Button(name="Patient Portal", button_type="light", on_click=show_chat),
    pn.widgets.Button(name="Staff Access", button_type="light", on_click=show_admin),
    css_classes=['header-bar'],
    sizing_mode="stretch_width"
)

# Patient Auth Flow (Redesigned)
auth_input = pn.widgets.PasswordInput(name="Portal Access Code", placeholder=f"Enter code ({ACCESS_CODE})")
auth_button = pn.widgets.Button(name="Access Secure Portal", button_type="primary", sizing_mode="stretch_width")
auth_error = pn.pane.Markdown("", styles={'color': '#e53e3e'})

def login_check(event):
    if auth_input.value == ACCESS_CODE:
        logger.info("Patient portal access granted.")
        show_chat()
    else:
        logger.warning("Portal access denied.")
        auth_error.object = "🚨 **Access Denied:** Please verify your clinic code."

auth_button.on_click(login_check)

auth_area = pn.Column(
    pn.pane.Markdown(f"""
    # Secure Patient Consultation
    Welcome to **{CLINIC_NAME}**. Please enter the clinic access code provided to you to begin your secure session.
    """),
    auth_input, auth_button, auth_error,
    css_classes=['chat-container'],
    styles={'max-width': '500px', 'margin': '100px auto', 'text-align': 'center'}
)

# Initialize with Auth
main_area.append(auth_area)

app_layout = pn.Column(
    nav_bar,
    main_area,
    sizing_mode="stretch_width",
    styles={'background-color': '#f7fafc', 'min-height': '100vh'}
)

if __name__ == "__main__":
    logger.info("Starting Premium BrightSmile DentalBot...")
    pn.serve(app_layout, title=CLINIC_NAME)
