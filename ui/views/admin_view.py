import panel as pn
import pandas as pd
from core.admin_logic import get_appointment_stats, export_appointments_to_csv, generate_recovery_message
from core.database import get_all_appointments
from config import ADMIN_PASSWORD

class AdminView:
    def __init__(self):
        self.auth_input = pn.widgets.PasswordInput(placeholder="Enter Staff Password")
        self.auth_button = pn.widgets.Button(name="Login", button_type="primary")
        self.auth_button.on_click(self.check_auth)
        self.error_msg = pn.pane.Markdown("", styles={'color': 'red'})

        self.auth_view = pn.Column(
            pn.pane.Markdown("### Staff Dashboard Access"),
            self.auth_input,
            self.auth_button,
            self.error_msg,
            css_classes=['chat-container']
        )
        
        self.dashboard_view = pn.Column(visible=False)
        self.layout = pn.Column(self.auth_view, self.dashboard_view)

    def check_auth(self, event):
        if self.auth_input.value == ADMIN_PASSWORD:
            self.auth_view.visible = False
            self.build_dashboard()
            self.dashboard_view.visible = True
        else:
            self.error_msg.object = "Invalid password."

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
        export_btn.on_click(lambda e: export_msg.update(object="✅ Exported!" if export_appointments_to_csv() else "❌ Failed"))

        overview_tab = pn.Column(
            pn.pane.Markdown("### 📊 Practice Analytics"),
            cards,
            pn.pane.Markdown("### 🗓️ Recent Appointments"),
            table,
            pn.Row(export_btn, export_msg)
        )

        # TAB 2: Recovery Tracker
        recovery_list = pn.Column(pn.pane.Markdown("### 🌡️ Recovery Follow-up Hub"), sizing_mode="stretch_width")
        
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
                ("📈 Overview", overview_tab),
                ("🌡️ Recovery Hub", recovery_list),
                sizing_mode="stretch_width"
            )
        )

    def get_layout(self):
        return self.layout
