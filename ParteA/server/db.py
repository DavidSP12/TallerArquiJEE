import os
import sqlite3
from typing import List, Dict

DB_PATH = os.getenv("SERVER_DB_PATH", "/data/server.db")


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

        count = conn.execute("SELECT COUNT(*) AS total FROM students").fetchone()["total"]
        if count == 0:
            conn.executemany(
                """
                INSERT INTO students (first_name, last_name, email, major)
                VALUES (?, ?, ?, ?)
                """,
                [
                    ("Ana", "Gomez", "ana.gomez@universidad.edu", "Arquitectura"),
                    ("Luis", "Perez", "luis.perez@universidad.edu", "Ingenieria de Sistemas"),
                    ("Marta", "Diaz", "marta.diaz@universidad.edu", "Matematicas"),
                    ("Carlos", "Rojas", "carlos.rojas@universidad.edu", "Fisica"),
                    ("Sofia", "Martinez", "sofia.martinez@universidad.edu", "Quimica"),
                ],
            )
        conn.commit()


def fetch_students() -> List[Dict[str, str]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, first_name, last_name, email, major
            FROM students
            ORDER BY id
            """
        ).fetchall()

    return [dict(row) for row in rows]
