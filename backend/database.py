import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "users.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                picture TEXT,
                google_id TEXT,
                google_access_token TEXT,
                google_refresh_token TEXT,
                youtube_access_token TEXT,
                youtube_refresh_token TEXT,
                twitch_access_token TEXT,
                twitch_refresh_token TEXT,
                vk_access_token TEXT,
                vk_refresh_token TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        existing_columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(users)").fetchall()
        }

        for column_name, column_definition in {
            "google_access_token": "TEXT",
            "google_refresh_token": "TEXT",
            "youtube_access_token": "TEXT",
            "youtube_refresh_token": "TEXT",
            "twitch_access_token": "TEXT",
            "twitch_refresh_token": "TEXT",
            "vk_access_token": "TEXT",
            "vk_refresh_token": "TEXT",
            "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
        }.items():
            if column_name not in existing_columns:
                conn.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}")

        conn.commit()


init_db()


def _normalize_user_data(user_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "email": user_data.get("email"),
        "name": user_data.get("name"),
        "picture": user_data.get("picture"),
        "google_id": user_data.get("google_id"),
        "google_access_token": user_data.get("google_access_token"),
        "google_refresh_token": user_data.get("google_refresh_token"),
        "youtube_access_token": user_data.get("youtube_access_token"),
        "youtube_refresh_token": user_data.get("youtube_refresh_token"),
        "twitch_access_token": user_data.get("twitch_access_token"),
        "twitch_refresh_token": user_data.get("twitch_refresh_token"),
        "vk_access_token": user_data.get("vk_access_token"),
        "vk_refresh_token": user_data.get("vk_refresh_token"),
    }


def upsert_user(user_data: dict[str, Any]) -> int:
    with get_connection() as conn:
        normalized_user_data = _normalize_user_data(user_data)
        existing = None

        if user_data.get("id") is not None:
            existing = conn.execute("SELECT id FROM users WHERE id = ?", (user_data["id"],)).fetchone()

        if not existing:
            existing = conn.execute(
                "SELECT id FROM users WHERE google_id = ? OR email = ?",
                (user_data.get("google_id"), user_data.get("email")),
            ).fetchone()

        if existing:
            conn.execute(
                """
                UPDATE users SET
                    email = COALESCE(:email, email),
                    name = COALESCE(:name, name),
                    picture = COALESCE(:picture, picture),
                    google_id = COALESCE(:google_id, google_id),
                    google_access_token = COALESCE(:google_access_token, google_access_token),
                    google_refresh_token = COALESCE(:google_refresh_token, google_refresh_token),
                    youtube_access_token = COALESCE(:youtube_access_token, youtube_access_token),
                    youtube_refresh_token = COALESCE(:youtube_refresh_token, youtube_refresh_token),
                    twitch_access_token = COALESCE(:twitch_access_token, twitch_access_token),
                    twitch_refresh_token = COALESCE(:twitch_refresh_token, twitch_refresh_token),
                    vk_access_token = COALESCE(:vk_access_token, vk_access_token),
                    vk_refresh_token = COALESCE(:vk_refresh_token, vk_refresh_token),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = :id
                """,
                {
                    **normalized_user_data,
                    "id": existing[0],
                },
            )
            conn.commit()
            return int(existing[0])

        cursor = conn.execute(
            """
            INSERT INTO users (
                email, name, picture, google_id, google_access_token, google_refresh_token,
                youtube_access_token, youtube_refresh_token, twitch_access_token, twitch_refresh_token,
                vk_access_token, vk_refresh_token
            ) VALUES (
                :email, :name, :picture, :google_id, :google_access_token, :google_refresh_token,
                :youtube_access_token, :youtube_refresh_token, :twitch_access_token, :twitch_refresh_token,
                :vk_access_token, :vk_refresh_token
            )
            """,
            normalized_user_data,
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def get_user_by_google_id(google_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE google_id = ?", (google_id,)).fetchone()
        return dict(row) if row else None
