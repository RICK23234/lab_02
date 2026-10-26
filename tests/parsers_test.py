from datetime import datetime
from pathlib import Path

import pytest

from scr.streamstats.errors import InvalidEventError, InvalidTimestampError, UnsupportedFormatError
from scr.streamstats.models import new_stats
from scr.streamstats.parsers import get_parser, parse_csv, parse_jsonl

DATA = Path(__file__).parent / "data"


def test_jsonl_valid_count():
    assert len(list(parse_jsonl(DATA / "valid.jsonl"))) == 4


def test_jsonl_event_fields():
    event = list(parse_jsonl(DATA / "valid.jsonl"))[0]
    assert (event["timestamp"], event["level"], event["source"]) == (datetime(2026, 1, 1, 12, 0), "INFO", "api")


def test_csv_valid_count():
    assert len(list(parse_csv(DATA / "valid.csv"))) == 4


def test_jsonl_invalid_raises():
    with pytest.raises(InvalidEventError):
        list(parse_jsonl(DATA / "invalid.jsonl"))


def test_skip_invalid():
    stats = new_stats()
    events = list(parse_jsonl(DATA / "invalid.jsonl", skip_invalid=True, stats=stats))
    assert (len(events), stats["skipped"]) == (2, 3)


def test_bad_timestamp_raises():
    with pytest.raises(InvalidTimestampError):
        list(parse_jsonl(DATA / "bad_timestamp.jsonl"))


def test_missing_column_raises():
    with pytest.raises(InvalidEventError):
        list(parse_csv(DATA / "missing_column.csv"))


def test_unsupport_format_raises():
    with pytest.raises(UnsupportedFormatError):
        get_parser("txt")
        