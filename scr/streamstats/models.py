from datetime import datetime
from collections import Counter

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

ERROR_LEVELS = ("ERROR", "CRITICAL")


def new_event(timestamp: datetime, level: str, sorce: str, message: str) -> dict:
    return {
        "timestamp": timestamp,
        "level": level,
        "source": sorce,
        "message": message,
    }


def new_stats() -> dict:
    return {
        "total": 0,
        "skipped": 0,
        "levels": Counter(),
        "sources": Counter(),
        "error_sources": Counter(),
        "first_timestamp": None,
        "last_timestamp": None,
    }