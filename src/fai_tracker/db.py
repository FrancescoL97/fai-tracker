from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS fai_records (
  id           TEXT PRIMARY KEY,
  pn           TEXT NOT NULL,
  issue_year   INTEGER NOT NULL,
  issue_month  INTEGER NOT NULL,
  folder_name  TEXT NOT NULL,
  path         TEXT NOT NULL,
  location     TEXT NOT NULL CHECK (location IN ('ACTIVE','ARCHIVED')),
  old_version  INTEGER,
  created_at   TEXT NOT NULL,
  updated_at   TEXT NOT NULL,
  archived_at  TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_active_per_pn
ON fai_records(pn)
WHERE location = 'ACTIVE';

CREATE INDEX IF NOT EXISTS ix_records_pn
ON fai_records(pn);

CREATE INDEX IF NOT EXISTS ix_records_issue
ON fai_records(issue_year, issue_month);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Create a SQLite connection with reasonable defaults."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # rows as dict-like objects
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Path) -> None:
    """Create DB file and schema if missing."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
