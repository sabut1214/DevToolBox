"""Extract links from text."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import typer

URL_PATTERN = re.compile(r"(?:https?://|ftp://|mailto:)[^\s\]\)>'\"}]+")
TRAILING_PUNCT = ".,);:]>\"'"


def _read_text(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    return path.read_text(encoding="utf-8")


def extract_links(
    path: Path | None = typer.Argument(
        None, help="Input file (.md or .txt). If omitted, reads stdin."
    ),
    domain_only: bool = typer.Option(
        False, "--domain-only", help="Print only unique domains."
    ),
    unique: bool = typer.Option(
        True, "--unique/--no-unique", help="Deduplicate output."
    ),
) -> None:
    """Extract URLs from a file or stdin."""
    try:
        text = _read_text(path)
    except FileNotFoundError:
        typer.echo(f"File not found: {path}", err=True)
        raise typer.Exit(code=1)

    matches = URL_PATTERN.findall(text)
    cleaned: list[str] = [match.rstrip(TRAILING_PUNCT) for match in matches]

    def emit(values: list[str]) -> None:
        if unique:
            seen: set[str] = set()
            for value in values:
                if value in seen:
                    continue
                seen.add(value)
                typer.echo(value)
            return
        for value in values:
            typer.echo(value)

    if domain_only:
        domains: list[str] = []
        for url in cleaned:
            parsed = urlparse(url)
            if parsed.scheme == "mailto":
                if "@" in parsed.path:
                    domains.append(parsed.path.split("@")[-1])
                continue
            if parsed.netloc:
                domains.append(parsed.netloc)
        emit(domains)
        return

    emit(cleaned)


def register(app: typer.Typer) -> None:
    app.command("extract-links")(extract_links)
