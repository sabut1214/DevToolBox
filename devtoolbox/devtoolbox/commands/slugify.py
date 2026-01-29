"""Slugify text."""

from __future__ import annotations

import sys
import unicodedata

import typer


def _is_word_char(char: str) -> bool:
    category = unicodedata.category(char)
    return category.startswith(("L", "N"))


def _collapse_separators(text: str, separator: str) -> str:
    while separator * 2 in text:
        text = text.replace(separator * 2, separator)
    return text.strip(separator)


def slugify_text(
    text: str,
    lower: bool = True,
    max_len: int | None = None,
    ascii_only: bool = True,
    separator: str = "-",
) -> str:
    if not separator:
        separator = "-"

    normalized = unicodedata.normalize("NFKD" if ascii_only else "NFKC", text)
    if ascii_only:
        normalized = normalized.encode("ascii", "ignore").decode("ascii")

    if lower:
        normalized = normalized.lower()

    pieces: list[str] = []
    for char in normalized:
        if _is_word_char(char):
            pieces.append(char)
        else:
            pieces.append(separator)

    slug = _collapse_separators("".join(pieces), separator)

    if max_len is not None and max_len > 0:
        slug = slug[:max_len].rstrip(separator)
    return slug


def slugify(
    text: str | None = typer.Argument(
        None, help="Text to slugify. If omitted, reads from stdin."
    ),
    lower: bool = typer.Option(True, "--lower/--no-lower", help="Lowercase output."),
    ascii_only: bool = typer.Option(
        True, "--ascii-only/--no-ascii-only", help="Strip non-ASCII characters."
    ),
    separator: str = typer.Option("-", "--separator", help="Separator character."),
    max_len: int | None = typer.Option(None, "--max-len", min=1, help="Max length."),
) -> None:
    """Convert text to a URL-friendly slug."""
    value = text if text is not None else sys.stdin.read()
    slug = slugify_text(
        value, lower=lower, max_len=max_len, ascii_only=ascii_only, separator=separator
    )
    typer.echo(slug)


def register(app: typer.Typer) -> None:
    app.command("slugify")(slugify)
