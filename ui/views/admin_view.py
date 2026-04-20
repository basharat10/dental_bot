import panel as pn
import pandas as pd
from core.admin_logic import get_appointment_stats, export_appointments_to_csv
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
        
        # Stats Cards
        cards = pn.Row(
            pn.Column(pn.pane.Markdown("#### Total"), pn.pane.Markdown(f"<span class='stat-value'>{stats['total']}</span>"), css_classes=['admin-card']),
            pn.Column(pn.pane.Markdown("#### Pending"), pn.pane.Markdown(f"<span class='stat-value'>{stats['pending']}</span>"), css_classes=['admin-card']),
            pn.Column(pn.pane.Markdown("#### Confirmed"), pn.pane.Markdown(f"<span class='stat-value'>{stats['confirmed']}</span>"), css_classes=['admin-card'])
        )

        # Data Table
        appointments = get_all_appointments()
        if appointments:
            df = pd.DataFrame(appointments)
            # Hide some internal columns if needed, or show all
            table = pn.widgets.Tabulator(df, pagination='remote', page_size=10, sizing_mode="stretch_width")
        else:
            table = pn.pane.Markdown("_No appointments found._")

        # Export Button
        export_btn = pn.widgets.Button(name="Export to CSV", button_type="success")
        export_msg = pn.pane.Markdown("")
        
        def do_export(event):
            if export_appointments_to_csv():
                export_msg.object = "Export successful! (appointments_export.csv)"
            else:
                export_msg.object = "Export failed."
                
        export_btn.on_click(do_export)

        self.dashboard_view.clear()
        self.dashboard_view.extend([
            pn.pane.Markdown("## 🏥 Clinic Management Dashboard"),
            cards,
            pn.pane.Markdown("### Recent Appointments"),
            table,
            pn.Row(export_btn, export_msg)
        ])

    def get_layout(self):
        return self.layout
