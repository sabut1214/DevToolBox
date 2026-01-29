from typer.testing import CliRunner

from devtoolbox.cli import app

runner = CliRunner()


def test_fmt_json_stdout(tmp_path):
    sample = tmp_path / "sample.json"
    sample.write_text('{"b":1,"a":2}', encoding="utf-8")

    result = runner.invoke(app, ["fmt-json", str(sample)])

    assert result.exit_code == 0
    assert '"a": 2' in result.stdout
    assert result.stdout.strip().startswith("{")


def test_fmt_json_in_place(tmp_path):
    sample = tmp_path / "sample.json"
    sample.write_text('{"b":1,"a":2}', encoding="utf-8")

    result = runner.invoke(app, ["fmt-json", str(sample), "--in-place"])

    assert result.exit_code == 0
    assert "Formatted" in result.stdout
    assert '"a": 2' in sample.read_text(encoding="utf-8")


def test_fmt_json_indent(tmp_path):
    sample = tmp_path / "sample.json"
    sample.write_text('{"a":1}', encoding="utf-8")

    result = runner.invoke(app, ["fmt-json", str(sample), "--indent", "4"])

    assert result.exit_code == 0
    assert "\n    \"a\": 1" in result.stdout


def test_fmt_json_no_sort_keys(tmp_path):
    sample = tmp_path / "sample.json"
    sample.write_text('{"b":1,"a":2}', encoding="utf-8")

    result = runner.invoke(app, ["fmt-json", str(sample), "--no-sort-keys"])

    assert result.exit_code == 0
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert lines[1].startswith('"b": 1')


def test_fmt_json_jsonl(tmp_path):
    sample = tmp_path / "sample.jsonl"
    sample.write_text('{"a":1}\n{"b":2}\n', encoding="utf-8")

    result = runner.invoke(app, ["fmt-json", str(sample)])

    assert result.exit_code == 0
    assert result.stdout.count("{") == 2


def test_fmt_json_jsonl_invalid_line(tmp_path):
    sample = tmp_path / "sample.jsonl"
    sample.write_text('{"a":1}\n{bad}\n', encoding="utf-8")

    result = runner.invoke(app, ["fmt-json", str(sample)])

    assert result.exit_code == 1
    assert "line 2" in result.stderr
