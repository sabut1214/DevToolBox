from typer.testing import CliRunner

from devtoolbox.cli import app

runner = CliRunner()


def test_slugify_basic():
    result = runner.invoke(app, ["slugify", "Hello, World!"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "hello-world"


def test_slugify_max_len():
    result = runner.invoke(app, ["slugify", "Hello World", "--max-len", "5"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "hello"
