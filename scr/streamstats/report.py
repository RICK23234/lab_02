import json

from .analysis import top_error_sources
from .models import LEVELS


def build_report(stats: dict, top_n: int = 5) -> dict:

    return {
        "total": stats["total"],
        "skipped_lines": stats["skipped"],
        "levels": {level: stats["levels"].get(level) for level in LEVELS},
        "sources": dict(sorted(stats["sources"].items())),
        "top_errors_sources": [
            {"source": source, "count": count} for source, count in top_error_sources(stats, top_n)

        ],
        "first_timestamp": stats["first_timestamp"] if stats["first_timestamp"] else None,
        "last_timestamp": stats["last_timestamp"] if stats["last_timestamp"] else None
    }


def report_to_str(report: dict) -> str:
    return json.dumps(report, default=str)


def write_report(report: dict, path) -> None:
    with open(path, "w") as file:
        file.write(report_to_str(report))
 