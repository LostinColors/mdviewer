#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_NAME="mdviewer"
PKG_VERSION="1.0.0-1"
PKG_DIR="${ROOT_DIR}/build/pkg"
DEB_FILE="${ROOT_DIR}/${PKG_NAME}_${PKG_VERSION}_all.deb"
DEPS_DIR="${PKG_DIR}/usr/lib/${PKG_NAME}/deps"

# ------------------------------------------------------------------
echo "=== Building self-contained .deb package for mdviewer ==="

# ---- clean ----
rm -rf "${PKG_DIR}" "${DEB_FILE}"

# ---- create package directory layout ----
mkdir -p "${PKG_DIR}/DEBIAN"
mkdir -p "${PKG_DIR}/usr/bin"
mkdir -p "${DEPS_DIR}"
mkdir -p "${PKG_DIR}/usr/lib/${PKG_NAME}/mdviewer"
mkdir -p "${PKG_DIR}/usr/share/doc/${PKG_NAME}"
mkdir -p "${PKG_DIR}/usr/share/man/man1"

# ---- copy mdviewer Python module ----
cp "${ROOT_DIR}/mdviewer/"*.py "${PKG_DIR}/usr/lib/${PKG_NAME}/mdviewer/"

# ---- download & vendor dependencies ----
echo "Downloading dependency wheels via pip..."
python3 -m pip download \
    --only-binary=:all: --no-deps \
    --dest /tmp/mdviewer-wheels \
    mistune pygments 2>&1 | tail -5

echo "Extracting vendored deps..."
for wheel in /tmp/mdviewer-wheels/mistune-*.whl /tmp/mdviewer-wheels/pygments-*.whl; do
    unzip -q -o "$wheel" -d "${DEPS_DIR}"
done

rm -rf /tmp/mdviewer-wheels

# ---- create launcher wrapper ----
cat > "${PKG_DIR}/usr/bin/${PKG_NAME}" << 'WRAPPER'
#!/bin/sh
PYTHONPATH="/usr/lib/mdviewer/deps:/usr/lib/mdviewer${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH
exec /usr/bin/python3 -m mdviewer "$@"
WRAPPER
chmod 755 "${PKG_DIR}/usr/bin/${PKG_NAME}"

# ---- DEBIAN/control ----
cat > "${PKG_DIR}/DEBIAN/control" << 'CONTROL'
Package: mdviewer
Version: 1.0.0-1
Section: text
Priority: optional
Architecture: all
Maintainer: mdviewer developers <dev@mdviewer.local>
Depends: python3 (>= 3.10)
Description: Markdown viewer that renders files in your browser
 mdviewer converts Markdown files to styled HTML pages with
 syntax highlighting and opens them in your default browser.
 It bundles all Python dependencies – no pip install required.
 .
 Features:
  * GitHub-like CSS theme
  * Syntax highlighting via Pygments
  * Heading anchors for easy navigation
  * Task lists, tables, footnotes, strikethrough
CONTROL

# ---- DEBIAN/postinst ----
cat > "${PKG_DIR}/DEBIAN/postinst" << 'POSTINST'
#!/bin/sh
set -e
echo " ✔ mdviewer installed!"
echo "    Usage: mdviewer path/to/file.md"
POSTINST
chmod 755 "${PKG_DIR}/DEBIAN/postinst"

# ---- man page ----
cat > "${PKG_DIR}/usr/share/man/man1/mdviewer.1" << 'MAN'
.TH MDVIEWER 1 "June 2026" "mdviewer 1.0.0" "User Commands"
.SH NAME
mdviewer \- render Markdown files in your browser
.SH SYNOPSIS
.B mdviewer
[\fI\,OPTIONS\/\fR] \fI\,FILE\/\fR
.SH DESCRIPTION
mdviewer converts a Markdown file to a styled HTML page and opens it in your default browser.
.SH OPTIONS
.TP
.B \-o, \-\-output FILE
Write HTML to FILE instead of opening browser.
.TP
.B \-\-no-browser
Render to a temp file but do not open the browser.
.TP
.B \-\-stdout
Print the rendered HTML to standard output.
.TP
.B \-\-title TITLE
Set the HTML page title (default: filename without extension).
.SH EXAMPLE
.B mdviewer README.md
.P
.B mdviewer --stdout notes.md > notes.html
.SH AUTHOR
Written by the mdviewer project.
MAN
gzip -9 -f "${PKG_DIR}/usr/share/man/man1/mdviewer.1"

# ---- build .deb ----
echo "Building .deb package..."
fakeroot dpkg-deb -b -Zgzip "${PKG_DIR}" "${DEB_FILE}"

# ---- verify ----
echo ""
echo "=== Package built successfully ==="
dpkg-deb --info "${DEB_FILE}"
echo ""
dpkg-deb --contents "${DEB_FILE}" | head -30
echo "..."

echo ""
echo "File: ${DEB_FILE}"
echo "Size: $(du -h "${DEB_FILE}" | cut -f1)"
echo ""
echo "To install: sudo dpkg -i ${DEB_FILE}"
