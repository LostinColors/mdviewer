import re
import sys
import tempfile
import webbrowser
from pathlib import Path

from mdviewer.theme import CSS, PYGMENTS_DARK_CSS


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
{pygments_css}
.heading-anchor {{
    opacity: 0;
    margin-left: 6px;
    font-size: 0.8em;
    text-decoration: none;
    color: #0969da;
}}
h1:hover .heading-anchor,
h2:hover .heading-anchor,
h3:hover .heading-anchor,
h4:hover .heading-anchor,
h5:hover .heading-anchor,
h6:hover .heading-anchor {{
    opacity: 1;
}}
</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>"""


def _make_highlighter():
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, guess_lexer
        from pygments.formatters import HtmlFormatter
        from pygments.util import ClassNotFound

        def _highlight(code: str, lang: str) -> str:
            try:
                lexer = get_lexer_by_name(lang, stripall=False)
            except ClassNotFound:
                try:
                    lexer = guess_lexer(code)
                except ClassNotFound:
                    return _escape_html(code)
            formatter = HtmlFormatter(cssclass="codehilite", nowrap=False)
            return highlight(code, lexer, formatter)

        return _highlight
    except ImportError:
        return None


_highlight_code = _make_highlighter()


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def _render_code_block(code: str, lang: str) -> str:
    if _highlight_code is not None:
        highlighted = _highlight_code(code, lang)
        return f"<div class=\"highlight\">{highlighted}</div>"
    escaped = _escape_html(code)
    return f"<pre><code>{escaped}</code></pre>"


def _make_mistune_renderer():
    from mistune.renderers.html import HTMLRenderer

    class PygmentsRenderer(HTMLRenderer):
        def block_code(self, code: str, info: str | None = None) -> str:
            lang = info.strip() if info else ""
            if _highlight_code is not None:
                highlighted = _highlight_code(code, lang)
                return f"<div class=\"highlight\">{highlighted}</div>"
            escaped = _escape_html(code)
            lang_attr = f' class="language-{lang}"' if lang else ""
            return f"<pre><code{lang_attr}>{escaped}</code></pre>\n"

    return PygmentsRenderer


def _render_markdown(text: str) -> str:
    try:
        import mistune

        renderer_cls = _make_mistune_renderer()
        renderer = renderer_cls()
        md = mistune.create_markdown(
            renderer=renderer,
            plugins=["strikethrough", "table", "task_lists", "footnotes", "url"],
        )
        return md(text)
    except ImportError:
        pass

    text = _escape_html(text)
    return f"<pre><code>{text}</code></pre>"


def _add_heading_anchors(html_body: str) -> str:
    def _replace_heading(m: re.Match) -> str:
        level = m.group(1)
        content = m.group(2)
        slug = content.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"\s+", "-", slug)
        slug = slug.strip("-")
        return f'<h{level} id="{slug}">{content}<a class="heading-anchor" href="#{slug}">#</a></h{level}>'

    return re.sub(
        r"<h([1-6])>(.*?)</h\1>",
        _replace_heading,
        html_body,
    )


def render_markdown_file(path: Path, title: str = "Markdown") -> str:
    text = path.read_text(encoding="utf-8")
    body = _render_markdown(text)
    body = _add_heading_anchors(body)
    html = HTML_TEMPLATE.format(
        title=title,
        css=CSS,
        pygments_css=PYGMENTS_DARK_CSS,
        body=body,
    )
    return html


def open_in_browser(html: str, no_browser: bool = False) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        prefix="mdviewer_",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(html)
        tmp_path = f.name

    path = Path(tmp_path).resolve().as_uri()

    if no_browser:
        print(f"Rendered to {path}", file=sys.stderr)
        return

    try:
        opened = webbrowser.open(path)
        if not opened:
            import subprocess
            subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        import subprocess
        subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
