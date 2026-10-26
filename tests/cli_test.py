import json
from pathlib import Path

from scr.streamstats.__main__ import main

DATA = Path(__file__).parent / "data"
VALID = str(DATA / "valid.jsonl")


def test_cli_analyze_write_file(tmp):
    output = tmp / "report.json"
    assert main(["analyze", VALID, "--format", "jsonl", "--output", str(output)]) == 0
    assert json.loads(output.read_text())["total"] == 4


def test_cli_analyze_write_file(capsys):
    assert main(["analyze", VALID, "--format", "jsonl"]) == 0
    assert json.loads(capsys.readouterr().out)["total"] == 4


def test_cli_missing_file(capsys):
    assert main(["analyze", str(DATA / "file.jsonl"), "--format", "jsonl"]) == 2
    assert capsys.readouterr().err != ""
    