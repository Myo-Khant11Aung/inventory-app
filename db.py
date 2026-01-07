import sqlite3
from pathlib import Path
import migrations

APP_DIR = Path.home() / ".inverntory_app"
APP_DIR.mkdir(exist_ok=True)

DB_PATH = APP_DIR / "inventory.db"

def connect_db():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initialize the database with required tables."""
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER NOT NULL
            )
        """)

        cur = conn.cursor()
        cur.execute("SELECT version FROM schema_version")
        row = cur.fetchone()
        current_version = row[0] if row else 0

        for i, migration in enumerate(migrations.MIGRATIONS, start=1):
            if i > current_version:
                conn.executescript(migration)
                cur.execute("DELETE FROM schema_version")
                cur.execute(
                    "INSERT INTO schema_version (version) VALUES (?)", (i,)
                )