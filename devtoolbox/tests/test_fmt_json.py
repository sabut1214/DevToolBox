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
