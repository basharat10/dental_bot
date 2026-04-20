import sqlite3
from pathlib import Path

# Path to database file
DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "dental_clinic.db"

def init_db():
    """Initializes the SQLite database and creates the appointments table."""
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()

def save_appointment(data):
    """
    Saves a dictionary of appointment data into the database with validation.
    """
    # Simple Validation
    required_fields = ['name', 'service', 'date', 'time']
    for field in required_fields:
        if not data.get(field) or len(str(data.get(field)).strip()) < 2:
            print(f"Validation failed: Missing or invalid {field}")
            return False

    try:
        conn = sqlite3.connect(DB_PATH)
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
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def get_all_appointments():
    """Returns a list of all appointments from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Database error: {e}")
        return []

# Initialize on import
init_db()
