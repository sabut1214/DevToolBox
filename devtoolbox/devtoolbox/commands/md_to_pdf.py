"""Convert Markdown to PDF."""

from __future__ import annotations

from pathlib import Path

import typer


def md_to_pdf(
    input_path: Path = typer.Argument(..., help="Markdown file to convert."),
    output: Path | None = typer.Option(
        None, "--output", "-o", help="Output PDF path."
    ),
) -> None:
    """Convert a Markdown file to PDF."""
    if not input_path.exists():
        typer.echo(f"File not found: {input_path}", err=True)
        raise typer.Exit(code=1)

    try:
        import markdown
    except ImportError:
        typer.echo("Missing dependency: markdown", err=True)
        raise typer.Exit(code=1)

    try:
        from weasyprint import HTML
    except ImportError:
        typer.echo("Missing dependency: weasyprint", err=True)
        raise typer.Exit(code=1)

    text = input_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        text,
        extensions=["extra", "tables", "fenced_code"],
        output_format="html5",
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{input_path.stem}</title>
  <style>
    body {{ font-family: sans-serif; line-height: 1.6; padding: 24px; }}
    code {{ font-family: monospace; }}
    pre {{ background: #f6f8fa; padding: 12px; overflow-x: auto; }}
    h1, h2, h3 {{ margin-top: 24px; }}
  </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    output_path = output or input_path.with_suffix(".pdf")
    HTML(string=html, base_url=str(input_path.parent)).write_pdf(str(output_path))
    typer.echo(f"Wrote {output_path}")


def register(app: typer.Typer) -> None:
    app.command("md-to-pdf")(md_to_pdf)
