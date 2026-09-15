import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "memorydata" / "memories.db"

print(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)
""")

cursor.execute(
    "INSERT INTO memories (content) VALUES (?)",
    ("用户正在学习 Agent",)
)

conn.commit()

cursor.execute("SELECT * FROM memories")

rows = cursor.fetchall()

print(rows)

conn.close()