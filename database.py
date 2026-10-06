"""Database layer: owns the SQLite connection and all SQL for the users table."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "eventaura.db"


class Database:
    def __init__(self, path=DB_PATH):
        self._path = str(path)
        self._create_tables()

    @contextmanager
    def _connection(self):
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _create_tables(self):
        with self._connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name     TEXT NOT NULL,
                    username      TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    email         TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    role          TEXT NOT NULL CHECK (role IN ('user', 'staff', 'admin')),
                    status        TEXT NOT NULL DEFAULT 'active'
                                  CHECK (status IN ('active', 'pending', 'rejected', 'deactivated')),
                    credentials   TEXT,
                    created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    # ---- queries (always parameterized) ----
    def insert_user(self, full_name, username, email, password_hash, role, status, credentials=None):
        with self._connection() as conn:
            cur = conn.execute(
                "INSERT INTO users (full_name, username, email, password_hash, role, status, credentials) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (full_name, username, email, password_hash, role, status, credentials),
            )
            return cur.lastrowid

    def find_by_login(self, identifier):
        """Find a user by username or email."""
        with self._connection() as conn:
            return conn.execute(
                "SELECT * FROM users WHERE username = ? OR email = ?", (identifier, identifier)
            ).fetchone()

    def username_exists(self, username):
        with self._connection() as conn:
            return conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone() is not None

    def email_exists(self, email):
        with self._connection() as conn:
            return conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone() is not None

    def count_role(self, role):
        with self._connection() as conn:
            return conn.execute("SELECT COUNT(*) FROM users WHERE role = ?", (role,)).fetchone()[0]
