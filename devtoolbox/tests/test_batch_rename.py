from typer.testing import CliRunner

from devtoolbox.cli import app

runner = CliRunner()


def test_batch_rename_dry_run(tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "batch-rename",
            str(tmp_path),
            "--prefix",
            "file_",
            "--start",
            "1",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert "a.txt -> file_1.txt" in result.stdout
    assert (tmp_path / "a.txt").exists()


def test_batch_rename_executes(tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")

    result = runner.invoke(
        app,
        ["batch-rename", str(tmp_path), "--prefix", "renamed_", "--start", "3"],
    )

    assert result.exit_code == 0
    assert (tmp_path / "renamed_3.txt").exists()
    assert (tmp_path / "renamed_4.txt").exists()
