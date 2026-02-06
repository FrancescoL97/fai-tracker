from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    # DEV defaults (we will make them configurable later)
    active_root: Path
    archive_root: Path
    db_path: Path


def default_settings() -> Settings:
    """Default settings for local development."""
    base = Path.home() / "FAI-Tracker-Dev"
    return Settings(
        active_root=base / "ACTIVE_FAI",
        archive_root=base / "ARCHIVED_FAI",
        db_path=base / "fai_tracker.db",
    )