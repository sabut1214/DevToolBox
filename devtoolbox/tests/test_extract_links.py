from typer.testing import CliRunner

from devtoolbox.cli import app

runner = CliRunner()


def test_extract_links_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text(
        """
Visit https://example.com and https://example.com.
Also see https://example.org/path.
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["extract-links", str(sample)])

    assert result.exit_code == 0
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert lines == ["https://example.com", "https://example.org/path"]


def test_extract_links_domain_only(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text(
        """
Docs: https://docs.example.com/page
Main: https://example.com
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["extract-links", str(sample), "--domain-only"])

    assert result.exit_code == 0
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert lines == ["docs.example.com", "example.com"]
