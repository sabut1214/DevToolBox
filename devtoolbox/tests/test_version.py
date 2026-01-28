from typer.testing import CliRunner

from devtoolbox import __version__
from devtoolbox.cli import app

runner = CliRunner()


def test_version_flag():
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == __version__
