"""Extract links from text."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import typer

URL_PATTERN = re.compile(r"https?://[^\s\]\)>'\"}]+")
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
) -> None:
    """Extract unique URLs from a file or stdin."""
    try:
        text = _read_text(path)
    except FileNotFoundError:
        typer.echo(f"File not found: {path}", err=True)
        raise typer.Exit(code=1)

    matches = URL_PATTERN.findall(text)
    cleaned = {match.rstrip(TRAILING_PUNCT) for match in matches}

    if domain_only:
        domains = {urlparse(url).netloc for url in cleaned if urlparse(url).netloc}
        for domain in sorted(domains):
            typer.echo(domain)
        return

    for url in sorted(cleaned):
        typer.echo(url)


def register(app: typer.Typer) -> None:
    app.command("extract-links")(extract_links)
