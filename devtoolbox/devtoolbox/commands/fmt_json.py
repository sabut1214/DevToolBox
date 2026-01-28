"""Format JSON input."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import typer


def _load_json(path: Path | None) -> object:
    if path is None:
        data = sys.stdin.read()
    else:
        data = path.read_text(encoding="utf-8")
    return json.loads(data)


def fmt_json(
    path: Path | None = typer.Argument(
        None, help="JSON file path. If omitted, reads from stdin."
    ),
    in_place: bool = typer.Option(False, "--in-place", help="Overwrite the file."),
) -> None:
    """Format JSON from a file or stdin."""
    try:
        payload = _load_json(path)
    except FileNotFoundError:
        typer.echo(f"File not found: {path}", err=True)
        raise typer.Exit(code=1)
    except json.JSONDecodeError as exc:
        typer.echo(f"Invalid JSON: {exc}", err=True)
        raise typer.Exit(code=1)

    formatted = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)

    if in_place:
        if path is None:
            typer.echo("Cannot use --in-place without a file path.", err=True)
            raise typer.Exit(code=1)
        path.write_text(f"{formatted}\n", encoding="utf-8")
        typer.echo(f"Formatted {path}")
        return

    typer.echo(formatted)


def register(app: typer.Typer) -> None:
    app.command("fmt-json")(fmt_json)
