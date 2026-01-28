"""Dev Toolbox command-line interface."""

import typer

from devtoolbox import __version__

from devtoolbox.commands import (
    batch_rename,
    extract_links,
    fmt_json,
    img_resize,
    md_to_pdf,
    slugify,
)

app = typer.Typer(help="Dev Toolbox CLI")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Dev Toolbox CLI."""


fmt_json.register(app)
slugify.register(app)
extract_links.register(app)
batch_rename.register(app)
md_to_pdf.register(app)
img_resize.register(app)


if __name__ == "__main__":
    app()
