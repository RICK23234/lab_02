from .models import ERROR_LEVELS, new_stats
from .parsers import get_parser


def update_stat(event: dict, stats: dict) -> None:
    """
    Функция для учета одно события
    """
    stats["total"] += 1
    stats["levels"][event["level"]] += 1
    stats["sources"][event["source"]] += 1

    if event["level"] in ERROR_LEVELS:
        stats["error_sources"][event["source"]] += 1

    first = stats["first_timestamp"]
    if first is None or event["timestamp"] < first:
        stats["first_timestamp"] = event["timestamp"]



def top_error_sources(stats: dict, n: int = 5) -> list:
    """
    Функция для возврата n источников
    """
    items = sorted(stats["error_sources"].items(), key=lambda item: (-item[1], item[0]))
    return items[:n]


def iter_events(paths: list, format: str, skip_invalid: bool, stats: dict):
    """
    Функция дает события из всех файлов
    """
    parser = get_parser(format)
    for path in paths:
        yield from parser(path, skip_invalid, stats)


def ananlyze(paths: list, format: str, skip_invalid: bool = False) -> dict:
    """
    Функция читает файлы и вохвращает статистику
    """
    stats = new_stats()

    for event in iter_events(paths, format, skip_invalid, stats):
        update_stat(event, stats)
    return stats
