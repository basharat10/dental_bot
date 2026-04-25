def normalize_appointment_payload(payload):
    if not isinstance(payload, dict):
        return None

    appointment = {
        "name": payload.get("name") or payload.get("patient_name"),
        "service": payload.get("service") or payload.get("procedure"),
        "date": payload.get("date") or payload.get("appointment_date"),
        "time": payload.get("time") or payload.get("appointment_time"),
        "notes": payload.get("notes") or payload.get("message") or "",
    }

    required = ("name", "service", "date", "time")
    if all(appointment.get(field) for field in required):
        return appointment
    return None
