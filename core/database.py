import sqlite3
from pathlib import Path
from core.logger import logger

# Path to database file
DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "dental_clinic.db"

def init_db():
    """Initializes the SQLite database and creates the appointments table."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                service TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                notes TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

        # Migration: Add columns if they don't exist
        try:
            cursor.execute("ALTER TABLE appointments ADD COLUMN status TEXT DEFAULT 'Pending'")
        except sqlite3.OperationalError as exc:
            if "duplicate column name" not in str(exc).lower():
                raise
        try:
            cursor.execute("ALTER TABLE appointments ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        except sqlite3.OperationalError as exc:
            if "duplicate column name" not in str(exc).lower():
                raise

        conn.commit()

def save_appointment(data):
    """
    Saves a dictionary of appointment data into the database with validation.
    """
    # Simple Validation
    required_fields = ['name', 'service', 'date', 'time']
    for field in required_fields:
        if not data.get(field) or len(str(data.get(field)).strip()) < 2:
            logger.warning("Appointment validation failed for field: %s", field)
            return False

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (name, service, appointment_date, appointment_time, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('name', ''),
                data.get('service', ''),
                data.get('date', ''),
                data.get('time', ''),
                data.get('notes', '')
            ))
            conn.commit()
            return True
    except Exception as e:
        logger.error("Database save error: %s", e)
        return False

def get_all_appointments():
    """Returns a list of all appointments from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM appointments ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        logger.error("Database read error: %s", e)
        return []

# Initialize on import
init_db()
