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


def test_slugify_separator():
    result = runner.invoke(app, ["slugify", "Hello World", "--separator", "_"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "hello_world"


def test_slugify_unicode_preserved():
    result = runner.invoke(
        app, ["slugify", "नमस्ते World", "--no-ascii-only", "--no-lower"]
    )

    assert result.exit_code == 0
    assert "नमस्ते" in result.stdout.strip()
