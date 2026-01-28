# Dev Toolbox CLI

Small, fast CLI utilities for everyday dev tasks: formatting JSON, slugifying text, extracting links, batch renaming files, converting Markdown to PDF, and resizing images.

## Install

Recommended (isolated global command):

```bash
pipx install .
```

Development install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## How to run

```bash
dt --help
```

## Commands

### fmt-json

```bash
dt fmt-json data.json
cat data.json | dt fmt-json

dt fmt-json data.json --in-place
```

### slugify

```bash
dt slugify "Hello, World!"
dt slugify "Hello World" --max-len 5
```

### extract-links

```bash
dt extract-links README.md

dt extract-links notes.txt --domain-only
```

### batch-rename

```bash
dt batch-rename ./photos --prefix img_ --start 1

dt batch-rename ./photos --prefix img_ --dry-run
```

### md-to-pdf

```bash
dt md-to-pdf docs/guide.md

dt md-to-pdf docs/guide.md --output docs/guide.pdf
```

### img-resize

```bash
dt img-resize logo.png --width 200

dt img-resize ./images --width 800 --height 600 --keep-aspect
```

## Screenshots / GIF

Add a short demo GIF here once you record one.

## License

MIT
