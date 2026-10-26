import json
import csv
import logging
from datetime import datetime

from .errors import InvalidEventError, InvalidTimestampError, UnsupportedFormatError
from .models import LEVELS, new_event

logger = logging.getLogger(__name__)

FIELDS = ("timestamp", "level", "source", "message")

def make_event(raw: dict, path, line_number: int) -> dict:
    timstamp_raw = raw.get("timestamp")
    if not isinstance(timstamp_raw, str) or not timstamp_raw.strip():
        raise InvalidTimestampError("Пустая дата", str(path), line_number, "timestamp")

    try:
        timestamp = datetime.fromisoformat(timstamp_raw.strip())
    except ValueError:
        raise InvalidTimestampError (f"Неверный формат даты {timstamp_raw}", str(path), line_number, "timestamp")

    level = raw.get("level")
    if level not in LEVELS:
        raise InvalidTimestampError(f"Неизветный уровень {level}", str(path), line_number, "level")

    source = raw.get("source")
    if not isinstance(source, str) or not source.strip():
        raise InvalidEventError("Нет источника", str(path), line_number, "source")

    message = raw.get("message")
    if not isinstance(message, str):
        raise InvalidEventError("Нет сообщения", str(path), line_number, "message")

    return new_event(timestamp, level, source, message)


def manage_invalid(error: InvalidEventError, skip_invalid: bool, stats) -> None:
    if not skip_invalid:
        raise error

    logging.warning("Пропущена строка: %s", error)
    if stats is not None:
        stats["skipped"] += 1



def parse_csv(path, skip_invalid: bool = False, stats=None):
    with open(path) as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            return

        missing = [name for name in FIELDS if name not in reader.fieldnames]
        if missing:
            raise InvalidEventError(f"В заголовке нет колонок {", ".join(missing)}", str(path), 1)

        for row in reader:
            try:
                event = make_event(row, path, reader.line_num)
            except InvalidEventError as error:
                manage_invalid(error, skip_invalid, stats)
                continue
            yield event


def parse_jsonl(path, skip_invalid: bool = False, stats = None):
    with open(path) as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                raw = json.loads(line)
            
                if not isinstance(raw, dict):
                    raise InvalidEventError("Строка должна быть JSON объектом", str(path), line_number)

                event = make_event(raw, path, line_number)

            except InvalidEventError as error:
                manage_invalid(error, skip_invalid, stats)
                continue
            yield event


PARSERS = {"csv": parse_csv, "jsonl": parse_jsonl}


def get_parser(format: str):
    if format not in PARSERS:
        raise UnsupportedFormatError(format)
    return PARSERS[format]