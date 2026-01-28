"""Slugify text."""

from __future__ import annotations

import re
import sys
import unicodedata

import typer


def slugify_text(text: str, lower: bool = True, max_len: int | None = None) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    if lower:
        ascii_text = ascii_text.lower()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-")
    slug = re.sub(r"-+", "-", slug)
    if max_len is not None and max_len > 0:
        slug = slug[:max_len].rstrip("-")
    return slug


def slugify(
    text: str | None = typer.Argument(
        None, help="Text to slugify. If omitted, reads from stdin."
    ),
    lower: bool = typer.Option(True, "--lower/--no-lower", help="Lowercase output."),
    max_len: int | None = typer.Option(None, "--max-len", min=1, help="Max length."),
) -> None:
    """Convert text to a URL-friendly slug."""
    value = text if text is not None else sys.stdin.read()
    slug = slugify_text(value, lower=lower, max_len=max_len)
    typer.echo(slug)


def register(app: typer.Typer) -> None:
    app.command("slugify")(slugify)
