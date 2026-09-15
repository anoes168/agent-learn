import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "memorydata" / "memories.db"

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        CONTENT TEXT NOT NULL
        )
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()