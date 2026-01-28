import pytest
from typer.testing import CliRunner

from devtoolbox.cli import app

runner = CliRunner()

markdown = pytest.importorskip("markdown")
weasyprint = pytest.importorskip("weasyprint")


def test_md_to_pdf_creates_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("# Title\n\nHello world.", encoding="utf-8")

    result = runner.invoke(app, ["md-to-pdf", str(sample)])

    assert result.exit_code == 0
    output_path = sample.with_suffix(".pdf")
    assert output_path.exists()
    assert output_path.stat().st_size > 0
