#!/bin/sh
set -e

echo "=== Installing mdviewer ==="

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required but not found."
    exit 1
fi

if ! python3 -c "import pip" >/dev/null 2>&1; then
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

echo "Installing dependencies and package..."
python3 -m pip install --user -e .

echo ""
echo "Installation complete!"
echo "Run 'mdviewer --help' to get started."
echo "Usage: mdviewer path/to/file.md"
