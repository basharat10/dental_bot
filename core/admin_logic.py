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

def generate_recovery_message(patient_name, procedure):
    """Generates a professional recovery check-in message."""
    messages = {
        "Cleaning": f"Hi {patient_name}, hope your teeth feel fresh after your cleaning! Remember to avoid dark liquids for a few hours. - BrightSmile Team",
        "Filling": f"Hi {patient_name}, just checking in after your filling. If you feel any high spots or sensitivity that doesn't fade, let us know! - BrightSmile Team",
        "Root Canal": f"Hi {patient_name}, it's been 24h since your root canal. Some soreness is normal, but if you have swelling or extreme pain, call us immediately! - BrightSmile Team",
        "Crown": f"Hi {patient_name}, hope your new crown is feeling comfortable. Avoid sticky foods on that side today. - BrightSmile Team"
    }
    return messages.get(procedure, f"Hi {patient_name}, just checking in on your recovery after your recent visit. How are you feeling? - BrightSmile Team")
