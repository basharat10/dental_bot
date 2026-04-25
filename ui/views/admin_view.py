import panel as pn
import pandas as pd
import hmac
import time
from core.admin_logic import get_appointment_stats, export_appointments_to_csv, generate_recovery_message
from core.database import get_all_appointments
from core.session import is_session_expired
from config import ADMIN_PASSWORD, ADMIN_SESSION_TIMEOUT_MINUTES

class AdminView:
    def __init__(self):
        self.failed_attempts = 0
        self.locked_until = 0.0
        self.last_activity_at = 0.0
        self.timeout_seconds = ADMIN_SESSION_TIMEOUT_MINUTES * 60
        self.timeout_callback = None
        self.auth_input = pn.widgets.PasswordInput(placeholder="Enter Staff Password")
        self.auth_button = pn.widgets.Button(name="Login", button_type="primary")
        self.auth_button.on_click(self.check_auth)
        self.error_msg = pn.pane.Markdown("", styles={'color': 'red'})

        self.auth_view = pn.Column(
            pn.pane.Markdown("### Staff Dashboard"),
            pn.pane.Markdown("Authorized team members only.", styles={"color": "#475569"}),
            self.auth_input,
            self.auth_button,
            self.error_msg,
            css_classes=['chat-container', 'admin-surface']
        )
        
        self.dashboard_view = pn.Column(visible=False)
        self.layout = pn.Column(self.auth_view, self.dashboard_view)

    def check_auth(self, event):
        now = time.time()
        if now < self.locked_until:
            wait_seconds = int(self.locked_until - now)
            self.error_msg.object = f"Too many failed attempts. Try again in {wait_seconds}s."
            return

        if hmac.compare_digest(self.auth_input.value or "", ADMIN_PASSWORD):
            self.failed_attempts = 0
            self.last_activity_at = now
            self.auth_view.visible = False
            self.build_dashboard()
            self.dashboard_view.visible = True
            self._start_timeout_monitor()
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 5:
                self.locked_until = now + 60
                self.failed_attempts = 0
                self.error_msg.object = "Too many failed attempts. Access is locked for 60 seconds."
                return
            self.error_msg.object = "Invalid password."

    def _touch_activity(self, event=None):
        self.last_activity_at = time.time()

    def _start_timeout_monitor(self):
        if self.timeout_callback:
            self.timeout_callback.stop()
        self.timeout_callback = pn.state.add_periodic_callback(self._check_session_timeout, period=5000)

    def _check_session_timeout(self):
        if not self.dashboard_view.visible:
            return
        if is_session_expired(self.last_activity_at, time.time(), self.timeout_seconds):
            self.logout_with_message("Session expired. Please log in again.")

    def logout_with_message(self, message):
        if self.timeout_callback:
            self.timeout_callback.stop()
            self.timeout_callback = None
        self.dashboard_view.visible = False
        self.dashboard_view.clear()
        self.auth_input.value = ""
        self.auth_view.visible = True
        self.error_msg.object = message
        self.last_activity_at = 0.0

    def build_dashboard(self):
        stats = get_appointment_stats()
        appointments = get_all_appointments()
        
        # TAB 1: Analytics Overview
        cards = pn.Row(
            pn.Column(pn.pane.Markdown("#### Total"), pn.pane.Markdown(f"<span class='stat-value'>{stats['total']}</span>"), css_classes=['admin-card']),
            pn.Column(pn.pane.Markdown("#### Pending"), pn.pane.Markdown(f"<span class='stat-value'>{stats['pending']}</span>"), css_classes=['admin-card']),
            pn.Column(pn.pane.Markdown("#### Confirmed"), pn.pane.Markdown(f"<span class='stat-value'>{stats['confirmed']}</span>"), css_classes=['admin-card'])
        )

        if appointments:
            df = pd.DataFrame(appointments)
            table = pn.widgets.Tabulator(df, pagination='remote', page_size=10, sizing_mode="stretch_width")
        else:
            table = pn.pane.Markdown("_No recent activity._")

        export_btn = pn.widgets.Button(name="Export to CSV", button_type="success")
        export_msg = pn.pane.Markdown("")
        def handle_export(event):
            self._touch_activity()
            export_msg.update(object="✅ Exported!" if export_appointments_to_csv() else "❌ Failed")

        export_btn.on_click(handle_export)
        logout_btn = pn.widgets.Button(name="Logout", button_type="light")
        logout_btn.on_click(lambda e: self.logout_with_message("Logged out successfully."))

        overview_tab = pn.Column(
            pn.pane.Markdown("### Practice Analytics"),
            cards,
            pn.pane.Markdown("### Recent Appointments"),
            table,
            pn.Row(export_btn, logout_btn, export_msg)
        )

        # TAB 2: Recovery Tracker
        recovery_list = pn.Column(pn.pane.Markdown("### Recovery Follow-up Hub"), sizing_mode="stretch_width")
        
        if appointments:
            # Filter for completed-looking appointments (e.g. status 'Confirmed' or older)
            for appt in appointments[:5]:  # Show latest 5 for recovery
                msg = generate_recovery_message(appt['name'], appt['service'])
                row = pn.Row(
                    pn.Column(
                        pn.pane.Markdown(f"**{appt['name']}** - {appt['service']}"),
                        pn.pane.Markdown(f"_{msg}_", styles={'font-size': '12px', 'color': '#718096'}),
                        css_classes=['admin-card'],
                        sizing_mode="stretch_width"
                    ),
                    pn.widgets.Button(name="Send via WhatsApp", button_type="primary", width=150),
                    pn.widgets.Button(name="Call Patient", button_type="light", width=120)
                )
                recovery_list.append(row)
        else:
            recovery_list.append(pn.pane.Markdown("_No patients pending recovery follow-up._"))

        self.dashboard_view.clear()
        self.dashboard_view.append(
            pn.Tabs(
                ("Overview", overview_tab),
                ("Recovery Hub", recovery_list),
                sizing_mode="stretch_width"
            )
        )

    def get_layout(self):
        return self.layout
