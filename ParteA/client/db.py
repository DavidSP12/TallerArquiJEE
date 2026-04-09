import os
import sqlite3
from typing import Iterable

DB_PATH = os.getenv("CLIENT_DB_PATH", "/data/client.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                major TEXT NOT NULL
            )
            """
        )
        conn.commit()


def upsert_students(students: Iterable) -> int:
    rows = [
        (s.id, s.first_name, s.last_name, s.email, s.major)
        for s in students
    ]

    if not rows:
        return 0

    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO students (id, first_name, last_name, email, major)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                email = excluded.email,
                major = excluded.major
            """,
            rows,
        )
        conn.commit()
    return len(rows)
