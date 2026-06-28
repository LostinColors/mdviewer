# mdviewer

A markdown viewer that renders files in your browser with syntax highlighting.

## Features

- Renders Markdown to styled HTML (GitHub-like theme).
- Syntax highlighting via Pygments (dark code blocks).
- Heading anchors for easy navigation.
- Supports task lists, tables, footnotes, strikethrough, blockquotes.
- Self-contained `.deb` package — no pip install needed.

## Quickstart

```bash
mdviewer README.md
```

This converts the file to HTML and opens it in your default browser.

## Install

### From .deb (Debian / Ubuntu)

```bash
sudo dpkg -i mdviewer_1.0.0.deb
```

### From source (any Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install mistune pygments
pip install -e .
mdviewer README.md
```

## How it works

1. Reads the Markdown file.
2. Parses it with [mistune](https://github.com/lepisma/mistune).
3. Applies Pygments syntax highlighting to code blocks.
4. Wraps in a styled HTML page (GitHub-inspired CSS).
5. Opens in your default browser via `xdg-open`.

Dependencies are vendored into the `.deb`/`.rpm` packages — no network access needed at install time.

## License

MIT
