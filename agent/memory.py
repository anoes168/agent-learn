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
        content TEXT NOT NULL
        )
        """)

    conn.commit()
    conn.close()

def save_memory(content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memories(CONTENT) VALUES (?)",
        (content,)
    )

    conn.commit()
    conn.close()
    return "memory saved"

def get_allmemory():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM memories"
    )

    row = cursor.fetchall()
    conn.close()
    return row

def get_memory_by_id(memory_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM memories WHERE id = ?",
        (memory_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

def update_memory(memory_id,new_content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE memories SET content = ? WHERE id = ?",
        (new_content, memory_id),
    )
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return success

def delete_memory(memory_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM memories WHERE id = ?",
        (memory_id,)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(save_memory("我爱你qwen"))
    print(get_allmemory())
    print(get_memory_by_id(1))
    update_memory(1,"我爱你")
    print(get_memory_by_id(1))
    print(delete_memory(1))
    print(get_allmemory())