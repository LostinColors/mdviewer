# mdviewer

A markdown viewer that renders files in your browser with syntax highlighting.

## Features

- Renders Markdown to styled HTML (GitHub-like theme)
- Syntax highlighting via Pygments (dark code blocks)
- Heading anchors for easy navigation
- Supports task lists, tables, footnotes, strikethrough, blockquotes
- Self-contained `.deb` package — no pip install needed

## Quickstart

```bash
mdviewer README.md
```

This converts the file to HTML and opens it in your default browser.

## Install

### From .deb (Debian / Ubuntu)

```bash
sudo dpkg -i mdviewer_1.0.0-1_all.deb
```

### From source (any Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install mistune pygments
pip install -e .
mdviewer README.md
```

## Usage

```
usage: mdviewer [-h] [-o OUTPUT] [--no-browser] [--title TITLE] [--stdout] file

Render a markdown file in your browser with syntax highlighting.

positional arguments:
  file                  Path to the markdown file (.md)

options:
  -h, --help            show this help message and exit
  -o, --output FILE     Write HTML output to a file instead of opening browser
  --no-browser          Render to HTML but do not open the browser
  --title TITLE         Custom title for the HTML page (default: filename)
  --stdout              Print HTML to stdout
```

### Examples

```bash
# Open in browser
mdviewer README.md

# Save to file
mdviewer doc.md -o output.html

# Pipe into a tool
mdviewer --stdout notes.md | wc -c

# Custom page title
mdviewer --title "My Doc" doc.md
```

## Build from source

### Debian package

```bash
./build_deb.sh
# produces: mdviewer_1.0.0-1_all.deb
```

### RPM (Fedora / RHEL)

```bash
sudo apt install rpm   # on Ubuntu
./build_rpm.sh
```

### Windows .exe

```bash
pip install pyinstaller
pyinstaller --onefile --name mdviewer mdviewer/__main__.py
# produces: dist/mdviewer.exe
```

## How it works

1. Reads the Markdown file
2. Parses it with [mistune](https://github.com/lepisma/mistune)
3. Applies Pygments syntax highlighting to code blocks
4. Wraps in a styled HTML page (GitHub-inspired CSS)
5. Opens in your default browser via `xdg-open`

Dependencies are vendored into the `.deb`/`.rpm` packages — no network access needed at install time.

## License

MIT
