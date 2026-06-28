import argparse
import sys
from pathlib import Path

from mdviewer.renderer import render_markdown_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a markdown file in your browser with syntax highlighting.",
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the markdown file (.md)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Write HTML output to a file instead of opening in browser",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Render to HTML but do not open the browser",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Custom title for the HTML page (default: filename)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print HTML to stdout instead of opening browser",
    )

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    if path.suffix.lower() not in (".md", ".markdown", ".mdown"):
        print(f"Warning: '{path}' may not be a markdown file", file=sys.stderr)

    title = args.title or path.stem

    html = render_markdown_file(path, title=title)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(html, encoding="utf-8")
        print(f"Written to {output_path.resolve()}")
        return

    if args.stdout:
        sys.stdout.write(html)
        return

    from mdviewer.renderer import open_in_browser
    open_in_browser(html, no_browser=args.no_browser)


if __name__ == "__main__":
    main()
