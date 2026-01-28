"""Batch rename files in a folder."""

from __future__ import annotations

from pathlib import Path

import typer


def _collect_files(folder: Path) -> list[Path]:
    return sorted([path for path in folder.iterdir() if path.is_file()])


def batch_rename(
    folder: Path = typer.Argument(..., help="Folder containing files to rename."),
    prefix: str = typer.Option("", help="Prefix for new filenames."),
    suffix: str = typer.Option("", help="Suffix for new filenames."),
    start: int = typer.Option(1, min=1, help="Starting index."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes."),
) -> None:
    """Rename files in a folder using prefix/suffix and numbering."""
    if not folder.exists() or not folder.is_dir():
        typer.echo(f"Folder not found: {folder}", err=True)
        raise typer.Exit(code=1)

    files = _collect_files(folder)
    if not files:
        typer.echo("No files found to rename.", err=True)
        raise typer.Exit(code=1)

    originals = {path.resolve() for path in files}
    planned: list[tuple[Path, Path]] = []
    for idx, path in enumerate(files, start=start):
        new_name = f"{prefix}{idx}{suffix}{path.suffix}"
        planned.append((path, folder / new_name))

    targets = [target.resolve() for _, target in planned]
    if len(targets) != len(set(targets)):
        typer.echo("Planned filenames are not unique.", err=True)
        raise typer.Exit(code=1)

    for source, target in planned:
        if target.exists() and target.resolve() not in originals:
            typer.echo(f"Target already exists: {target}", err=True)
            raise typer.Exit(code=1)

    for source, target in planned:
        typer.echo(f"{source.name} -> {target.name}")

    if dry_run:
        return

    temp_paths: list[tuple[Path, Path]] = []
    for idx, (source, target) in enumerate(planned):
        tmp_name = f".dtbox_tmp_{idx}_{source.name}"
        tmp_path = source.with_name(tmp_name)
        if tmp_path.exists():
            typer.echo(f"Temp path already exists: {tmp_path}", err=True)
            raise typer.Exit(code=1)
        source.rename(tmp_path)
        temp_paths.append((tmp_path, target))

    for tmp_path, target in temp_paths:
        tmp_path.rename(target)


def register(app: typer.Typer) -> None:
    app.command("batch-rename")(batch_rename)
