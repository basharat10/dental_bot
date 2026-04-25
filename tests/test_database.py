from pathlib import Path

from core import database


def test_save_and_get_appointment(tmp_path):
    database.DB_DIR = Path(tmp_path)
    database.DB_PATH = database.DB_DIR / "test_dental.db"
    database.init_db()

    saved = database.save_appointment(
        {
            "name": "Jane Smith",
            "service": "Cleaning",
            "date": "2026-04-24",
            "time": "11:00",
            "notes": "N/A",
        }
    )
    assert saved is True

    rows = database.get_all_appointments()
    assert len(rows) == 1
    assert rows[0]["name"] == "Jane Smith"
