from datetime import datetime
from pathlib import Path

from scr.streamstats.analysis import ananlyze, top_error_sources

DATA = Path(__file__).parent / "data"
VALID = DATA / "valid.jsonl"
SECOND = DATA / "second.jsonl"


def test_total():
    assert ananlyze([VALID], "jsonl")["total"] == 4


def test_levels_count():
    assert ananlyze([VALID], "jsonl")["levels"]["ERROR"] == 2


def test_source_count():
    assert ananlyze([VALID], "jsonl")["sources"] == {"api": 1, "db": 2, "auth": 1}


def test_top_error_source():
    stats = ananlyze([VALID], "jsonl")
    assert top_error_sources(stats) == [("db", 2), ("auth", 1)]


def test_two_files_first_timestamp():
    stats = ananlyze([VALID, SECOND], "jsonl")
    assert(stats["total"], stats["first_timestamp"]) == (6, datetime(2025, 12, 31, 23, 59))
