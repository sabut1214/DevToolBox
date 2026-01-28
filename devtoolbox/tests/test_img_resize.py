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
