import sqlite3
from datetime import datetime

DB_NAME = "chat_logs.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                intent TEXT,
                score REAL,
                timestamp TEXT
            )
        """)
    conn.commit()
    conn.close()

def save_log(session_id, user_message, bot_response, intent, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_logs (session_id, user_message, bot_response, intent, score, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, user_message, bot_response, intent, score, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()


def get_logs(limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, session_id, user_message, intent, score, timestamp FROM chat_logs ORDER BY id DESC LIMIT ?",
                   (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    save_log("test-session", "hello", "Hi there!", "greeting", 0.95)

    for row in get_logs():
        print(row)
        


