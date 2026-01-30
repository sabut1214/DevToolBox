"""Resize images."""

from __future__ import annotations

from pathlib import Path

import typer

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}


def _collect_images(path: Path, recursive: bool) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        iterator = path.rglob("*") if recursive else path.iterdir()
        return sorted(
            [
                child
                for child in iterator
                if child.is_file() and child.suffix.lower() in IMAGE_EXTS
            ]
        )
    return []


def _normalize_format(value: str | None) -> tuple[str | None, str | None]:
    if not value:
        return None, None
    cleaned = value.lstrip(".").lower()
    if cleaned == "jpg":
        cleaned = "jpeg"
    return cleaned, cleaned.upper()


def img_resize(
    input_path: Path = typer.Argument(..., help="Image file or folder."),
    width: int | None = typer.Option(None, "--width", min=1, help="Target width."),
    height: int | None = typer.Option(None, "--height", min=1, help="Target height."),
    keep_aspect: bool = typer.Option(
        True, "--keep-aspect/--no-keep-aspect", help="Preserve aspect ratio."
    ),
    output_format: str | None = typer.Option(
        None, "--format", help="Output format (e.g., png, jpeg)."
    ),
    output_dir: Path | None = typer.Option(
        None, "--output-dir", help="Directory for resized images."
    ),
    recursive: bool = typer.Option(
        False, "--recursive", help="Recurse into subfolders."
    ),
) -> None:
    """Resize image(s) to the desired dimensions."""
    if width is None and height is None:
        typer.echo("Provide --width, --height, or both.", err=True)
        raise typer.Exit(code=1)

    if not input_path.exists():
        typer.echo(f"Input not found: {input_path}", err=True)
        raise typer.Exit(code=1)

    try:
        from PIL import Image, ImageOps
    except ImportError:
        typer.echo("Missing dependency: Pillow. Install with: pip install Pillow", err=True)
        raise typer.Exit(code=1)

    images = _collect_images(input_path, recursive)
    if not images:
        typer.echo("No images found to resize.", err=True)
        raise typer.Exit(code=1)

    out_dir = output_dir or (
        input_path.parent / "resized" if input_path.is_file() else input_path / "resized"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    base_root = input_path.parent if input_path.is_file() else input_path
    ext, fmt = _normalize_format(output_format)

    for path in images:
        rel_path = path.name if input_path.is_file() else path.relative_to(base_root)
        with Image.open(path) as img:
            if keep_aspect:
                if width is not None and height is not None:
                    resized = ImageOps.contain(img, (width, height))
                elif width is not None:
                    new_height = round(img.height * (width / img.width))
                    resized = img.resize((width, new_height))
                else:
                    new_width = round(img.width * (height / img.height))
                    resized = img.resize((new_width, height))
            else:
                target_width = width or img.width
                target_height = height or img.height
                resized = img.resize((target_width, target_height))

            output_path = out_dir / rel_path
            if ext:
                output_path = output_path.with_suffix(f".{ext}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if fmt:
                resized.save(output_path, format=fmt)
            else:
                resized.save(output_path)
            typer.echo(str(output_path))


def register(app: typer.Typer) -> None:
    app.command("img-resize")(img_resize)
