from core.booking_parser import normalize_appointment_payload


def test_normalize_appointment_payload_maps_aliases():
    payload = {
        "patient_name": "John Doe",
        "procedure": "Cleaning",
        "appointment_date": "2026-04-25",
        "appointment_time": "10:30",
        "message": "First time patient",
    }
    normalized = normalize_appointment_payload(payload)
    assert normalized == {
        "name": "John Doe",
        "service": "Cleaning",
        "date": "2026-04-25",
        "time": "10:30",
        "notes": "First time patient",
    }


def test_normalize_appointment_payload_requires_required_fields():
    payload = {"name": "John Doe", "service": "Cleaning"}
    assert normalize_appointment_payload(payload) is None
