import pandas as pd
from core.database import get_all_appointments
from core.logger import logger

def get_appointment_stats():
    """Calculates statistics for the admin dashboard."""
    appointments = get_all_appointments()
    if not appointments:
        return {"total": 0, "pending": 0, "confirmed": 0}
    
    df = pd.DataFrame(appointments)
    stats = {
        "total": len(df),
        "pending": len(df[df['status'] == 'Pending']),
        "confirmed": len(df[df['status'] == 'Confirmed'])
    }
    return stats

def export_appointments_to_csv(filename="appointments_export.csv"):
    """Exports all appointments to a CSV file."""
    try:
        appointments = get_all_appointments()
        if not appointments:
            return False
        
        df = pd.DataFrame(appointments)
        df.to_csv(filename, index=False)
        logger.info(f"Appointments exported to {filename}")
        return True
    except Exception as e:
        logger.error(f"Export error: {e}")
        return False
