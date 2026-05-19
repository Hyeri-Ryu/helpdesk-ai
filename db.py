"""SQLite 기반 티켓 저장소

가벼운 파일 DB 하나로 시작 → 나중에 PostgreSQL/MySQL로 확장 가능.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "tickets.db"


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    """테이블이 없으면 생성"""
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                category TEXT,
                priority TEXT,
                summary TEXT,
                auto_reply TEXT,
                needs_human INTEGER,
                created_at TEXT NOT NULL
            )
            """
        )


def save_ticket(content: str, result: dict, created_at: str | None = None):
    init_db()
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO tickets
              (content, category, priority, summary, auto_reply, needs_human, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                content,
                result.get("category", "기타"),
                result.get("priority", "보통"),
                result.get("summary", ""),
                result.get("auto_reply", ""),
                1 if result.get("needs_human") else 0,
                created_at or datetime.now().isoformat(timespec="seconds"),
            ),
        )


def load_all_tickets() -> pd.DataFrame:
    init_db()
    with _conn() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM tickets ORDER BY created_at DESC", conn
        )
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"])
    return df


def clear_tickets():
    init_db()
    with _conn() as conn:
        conn.execute("DELETE FROM tickets")
