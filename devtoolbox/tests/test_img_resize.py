import pytest
from typer.testing import CliRunner

from devtoolbox.cli import app

runner = CliRunner()

PIL = pytest.importorskip("PIL")


def test_img_resize_output(tmp_path):
    from PIL import Image

    image_path = tmp_path / "sample.png"
    image = Image.new("RGB", (100, 50), color="red")
    image.save(image_path)

    result = runner.invoke(app, ["img-resize", str(image_path), "--width", "50"])

    assert result.exit_code == 0
    output_dir = tmp_path / "resized"
    output_path = output_dir / "sample.png"
    assert output_path.exists()


def test_img_resize_format_and_recursive(tmp_path):
    from PIL import Image

    nested = tmp_path / "images" / "nested"
    nested.mkdir(parents=True)
    image_path = nested / "sample.png"
    image = Image.new("RGB", (100, 50), color="blue")
    image.save(image_path)

    result = runner.invoke(
        app,
        [
            "img-resize",
            str(tmp_path / "images"),
            "--width",
            "50",
            "--format",
            "jpg",
            "--recursive",
        ],
    )

    assert result.exit_code == 0
    output_dir = tmp_path / "images" / "resized"
    output_path = output_dir / "nested" / "sample.jpg"
    assert output_path.exists()
