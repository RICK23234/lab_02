import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from .analysis import ananlyze
from .report import build_report, report_to_str, write_report
from .errors import CLIConfigError, StreamStatsError


def build():
    parser = ArgumentParser(prog="streamstats")
    subparser = parser.add_subparsers(dest="command", required=True)

    ananlyze_parser = subparser.add_parser(name="analyze", help="вывести статистику")
    ananlyze_parser.add_argument("inputs", nargs="+")
    ananlyze_parser.add_argument("--format", required=True, choices=["csv", "jsonl"])
    ananlyze_parser.add_argument("--output")
    ananlyze_parser.add_argument("--skip_invalid", action="store_true")
    ananlyze_parser.add_argument("--top", default=5)

    return parser


def run_analyze(arg):
    if arg.top < 1:
        raise CLIConfigError("В --top должно быть положительное число")

    paths = [Path(path) for path in arg.inputs]

    for path in paths:
        if path.is_file() == False:
            raise CLIConfigError(f"Нет такого файла {path}")

    stats = ananlyze(paths, arg.format, arg.skip_invalid)
    report = build_report(stats, arg.top)

    if arg.output:
        try:
            write_report(report, Path(arg.output))

        except OSError as error:
            raise CLIConfigError(f"Не удалось записать отчет: {error}")
            

    else:
        print(report_to_str(report))


def main(arg=None):
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    parser = build()
    arguments = parser.parse_args(arg)

    try:
        if arguments.command == "analyze":
            run_analyze(arguments)
    except StreamStatsError as error:
        print(f"\033[1;91mОшибка: {error} \033[0m", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())