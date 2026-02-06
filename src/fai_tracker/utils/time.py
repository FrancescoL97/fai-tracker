from __future__ import annotations

from datetime import datetime, timezone


def now_iso() -> str:
    """Return current UTC time in ISO 8601 format (e.g. 2026-02-06T14:22:10Z)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")