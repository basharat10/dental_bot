import panel as pn
import hmac
from core.logger import logger

APP_TITLE = "BrightSmile Dental Clinic"

try:
    from config import CLINIC_NAME, ACCESS_CODE
    from ui.styles import apply_styles
    from ui.views.chat_view import ChatView
    from ui.views.admin_view import AdminView

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
        pn.pane.Markdown(f"### 🦷 **{CLINIC_NAME}**", css_classes=["brand-title"]),
        pn.Spacer(),
        pn.widgets.Button(name="Consultation", button_type="primary", on_click=show_chat, width=130, css_classes=["nav-btn"]),
        pn.widgets.Button(name="Staff Access", button_type="primary", on_click=show_admin, width=130, css_classes=["nav-btn"]),
        sizing_mode="stretch_width",
        css_classes=["top-nav"]
    )

    # Login Hero Screen
    auth_input = pn.widgets.PasswordInput(placeholder="Invitation Code", width=300, align="center")
    auth_button = pn.widgets.Button(name="Access Secure Portal", button_type="primary", width=300, align="center")
    auth_error = pn.pane.Markdown("", styles={'color': '#ef4444'})

    def login_check(event):
        if hmac.compare_digest(auth_input.value or "", ACCESS_CODE):
            show_chat()
        else:
            auth_error.object = "Invalid invitation code."

    auth_button.on_click(login_check)

    auth_area = pn.Column(
        pn.pane.Markdown(f"# Welcome to {CLINIC_NAME}"),
        pn.pane.Markdown("Secure patient portal access.", styles={'color': '#64748b'}),
        auth_input, auth_button, auth_error,
        css_classes=['chat-container'],
        styles={'text-align': 'center'}
    )

    main_area.append(auth_area)
    APP_TITLE = CLINIC_NAME
    app_layout = pn.Column(nav_bar, main_area, sizing_mode="stretch_width", css_classes=["app-shell"])
except Exception as exc:
    logger.error("Application startup failed: %s", exc)
    app_layout = pn.Column(
        pn.pane.Markdown("# Configuration Error"),
        pn.pane.Markdown(
            "Application startup failed due to missing or invalid environment configuration. "
            "Please check your `.env` file and restart the app."
        ),
        pn.pane.Markdown(f"**Details:** `{exc}`"),
        sizing_mode="stretch_width",
        styles={"padding": "40px"},
    )

# Required when launched via `panel serve app.py`
app_layout.servable()

if __name__ == "__main__":
    logger.info("Launching Sleek BrightSmile Portal...")
    pn.serve(app_layout, title=APP_TITLE)
