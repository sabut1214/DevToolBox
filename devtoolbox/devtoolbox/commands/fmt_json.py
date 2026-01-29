"""Format JSON input."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import typer


def _read_text(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    return path.read_text(encoding="utf-8")


def _format_json(
    payload: object, indent: int, sort_keys: bool, ensure_ascii: bool
) -> str:
    return json.dumps(
        payload, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii
    )


def _format_jsonl(
    text: str, indent: int, sort_keys: bool, ensure_ascii: bool
) -> list[str]:
    lines = text.splitlines()
    output: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            output.append("")
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise json.JSONDecodeError(
                f"{exc.msg} (line {idx})", exc.doc, exc.pos
            ) from exc
        output.append(_format_json(payload, indent, sort_keys, ensure_ascii))
    return output


def fmt_json(
    path: Path | None = typer.Argument(
        None, help="JSON file path. If omitted, reads from stdin."
    ),
    in_place: bool = typer.Option(False, "--in-place", help="Overwrite the file."),
    indent: int = typer.Option(2, "--indent", min=0, help="Indent width."),
    sort_keys: bool = typer.Option(
        True, "--sort-keys/--no-sort-keys", help="Sort keys in output."
    ),
    jsonl: bool = typer.Option(
        False,
        "--jsonl/--no-jsonl",
        help="Treat input as JSON Lines (.jsonl).",
    ),
) -> None:
    """Format JSON from a file or stdin."""
    try:
        text = _read_text(path)
    except FileNotFoundError:
        typer.echo(f"File not found: {path}", err=True)
        raise typer.Exit(code=1)
    is_jsonl = jsonl or (path is not None and path.suffix.lower() == ".jsonl")

    try:
        if is_jsonl:
            formatted_lines = _format_jsonl(text, indent, sort_keys, ensure_ascii=False)
            formatted = "\n".join(formatted_lines)
        else:
            payload = json.loads(text)
            formatted = _format_json(payload, indent, sort_keys, ensure_ascii=False)
    except json.JSONDecodeError as exc:
        typer.echo(f"Invalid JSON: {exc}", err=True)
        raise typer.Exit(code=1)

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
