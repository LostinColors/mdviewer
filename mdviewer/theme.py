CSS = """\
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #1f2328;
    background-color: #ffffff;
    padding: 0;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 24px;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}

h1 { font-size: 2em; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; }
h2 { font-size: 1.5em; border-bottom: 1px solid #d0d7de; padding-bottom: 6px; }
h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: 0.875em; }
h6 { font-size: 0.85em; color: #656d76; }

p, ul, ol, dl, table, pre, blockquote {
    margin-top: 0;
    margin-bottom: 16px;
}

a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }

ul, ol {
    padding-left: 2em;
}

li { word-wrap: break-word; }
li + li { margin-top: 4px; }

blockquote {
    padding: 4px 16px;
    color: #656d76;
    border-left: 4px solid #d0d7de;
}

hr {
    height: 1px;
    padding: 0;
    margin: 24px 0;
    background-color: #d0d7de;
    border: 0;
}

table {
    display: block;
    width: 100%;
    max-width: 100%;
    overflow: auto;
    border-collapse: collapse;
}

table th {
    font-weight: 600;
}

table th, table td {
    padding: 8px 13px;
    border: 1px solid #d0d7de;
}

table tr { background-color: #ffffff; border-top: 1px solid #d0d7de; }
table tr:nth-child(2n) { background-color: #f6f8fa; }

img {
    max-width: 100%;
}

code {
    padding: 2px 6px;
    font-family: "SF Mono", "Cascadia Code", "Fira Code", "Consolas", "Liberation Mono", Menlo, monospace;
    font-size: 0.85em;
    background-color: #eef1f5;
    border-radius: 4px;
}

pre {
    background-color: #0d1117;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
}

pre code {
    padding: 0;
    background: none;
    font-size: 0.85em;
    line-height: 1.45;
    color: #e6edf3;
    border-radius: 0;
}

.highlight {
    background-color: #0d1117;
    border-radius: 6px;
    margin-bottom: 16px;
}

pre > code .linenos {
    color: #6e7681;
    padding-right: 16px;
    user-select: none;
}

.task-list-item {
    list-style: none;
}

.task-list-item input[type="checkbox"] {
    margin: 0 4px 0 -1.5em;
}

kbd {
    display: inline-block;
    padding: 3px 6px;
    font: 0.85em monospace;
    color: #1f2328;
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    box-shadow: inset 0 -1px 0 #d0d7de;
}

.footnotes {
    border-top: 1px solid #d0d7de;
    margin-top: 32px;
    padding-top: 16px;
    font-size: 0.85em;
    color: #656d76;
}

.footnotes ol { padding-left: 16px; }
.footnotes li:target { background-color: #fff8c5; }
"""
"""
Pygments CSS for dark code blocks will be injected at render time.
"""
PYGMENTS_DARK_CSS = """\
.codehilite .c, .codehilite .c1, .codehilite .cm, .codehilite .cs { color: #6e7681; font-style: italic; }
.codehilite .k, .codehilite .kd, .codehilite .kn, .codehilite .kp, .codehilite .kr, .codehilite .kt { color: #ff7b72; }
.codehilite .kc, .codehilite .kv { color: #79c0ff; }
.codehilite .n, .codehilite .na, .codehilite .nb, .codehilite .bp { color: #e6edf3; }
.codehilite .nc, .codehilite .no { color: #ffa657; }
.codehilite .nd { color: #d2a8ff; }
.codehilite .ni { color: #ffa657; }
.codehilite .ne, .codehilite .nf, .codehilite .nx { color: #d2a8ff; }
.codehilite .nl, .codehilite .nn { color: #ffa657; }
.codehilite .nt { color: #7ee787; }
.codehilite .nv, .codehilite .vc, .codehilite .vg, .codehilite .vi, .codehilite .vm { color: #e6edf3; }
.codehilite .o, .codehilite .ow { color: #ff7b72; }
.codehilite .p { color: #e6edf3; }
.codehilite .m, .codehilite .mb, .codehilite .mf, .codehilite .mh, .codehilite .mi, .codehilite .mo, .codehilite .mx { color: #79c0ff; }
.codehilite .s, .codehilite .s1, .codehilite .s2, .codehilite .sb, .codehilite .sc, .codehilite .sd, .codehilite .se, .codehilite .sh, .codehilite .si, .codehilite .sr, .codehilite .ss, .codehilite .sx { color: #a5d6ff; }
.codehilite .dl { color: #a5d6ff; }
.codehilite .sa { color: #ff7b72; }
.codehilite .gs { font-weight: bold; }
.codehilite .ge { font-style: italic; }
.codehilite .gh { color: #e6edf3; font-weight: bold; }
.codehilite .gu { color: #e6edf3; font-weight: bold; }
.codehilite .gd { color: #ffa198; background-color: #490202; }
.codehilite .gi { color: #7ee787; background-color: #04260f; }
.codehilite .go { color: #6e7681; }
.codehilite .gp { color: #6e7681; }
.codehilite .gr { color: #ffa198; }
.codehilite .gt { color: #ffa198; }
.codehilite .w { color: #6e7681; }
.codehilite .il { color: #79c0ff; }
"""
"""
GitHub-style Pygments CSS for light backgrounds.
"""
PYGMENTS_LIGHT_CSS = """\
.codehilite .c, .codehilite .c1, .codehilite .cm, .codehilite .cs { color: #6e7781; font-style: italic; }
.codehilite .k, .codehilite .kd, .codehilite .kn, .codehilite .kp, .codehilite .kr, .codehilite .kt { color: #cf222e; }
.codehilite .kc, .codehilite .kv { color: #0550ae; }
.codehilite .n, .codehilite .na, .codehilite .nb, .codehilite .bp { color: #1f2328; }
.codehilite .nc, .codehilite .no { color: #953800; }
.codehilite .nd { color: #8250df; }
.codehilite .ni { color: #953800; }
.codehilite .ne, .codehilite .nf, .codehilite .nx { color: #8250df; }
.codehilite .nl, .codehilite .nn { color: #953800; }
.codehilite .nt { color: #116329; }
.codehilite .nv, .codehilite .vc, .codehilite .vg, .codehilite .vi, .codehilite .vm { color: #1f2328; }
.codehilite .o, .codehilite .ow { color: #cf222e; }
.codehilite .p { color: #1f2328; }
.codehilite .m, .codehilite .mb, .codehilite .mf, .codehilite .mh, .codehilite .mi, .codehilite .mo, .codehilite .mx { color: #0550ae; }
.codehilite .s, .codehilite .s1, .codehilite .s2, .codehilite .sb, .codehilite .sc, .codehilite .sd, .codehilite .se, .codehilite .sh, .codehilite .si, .codehilite .sr, .codehilite .ss, .codehilite .sx { color: #0a3069; }
.codehilite .dl { color: #0a3069; }
.codehilite .sa { color: #cf222e; }
.codehilite .gs { font-weight: bold; }
.codehilite .ge { font-style: italic; }
.codehilite .gh { color: #1f2328; font-weight: bold; }
.codehilite .gu { color: #1f2328; font-weight: bold; }
.codehilite .gd { color: #82071e; background-color: #ffebe9; }
.codehilite .gi { color: #116329; background-color: #dafbe1; }
.codehilite .go { color: #6e7781; }
.codehilite .gp { color: #6e7781; }
.codehilite .gr { color: #82071e; }
.codehilite .gt { color: #82071e; }
.codehilite .w { color: #6e7781; }
.codehilite .il { color: #0550ae; }
"""
