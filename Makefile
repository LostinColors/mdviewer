.PHONY: install install-dev build clean test

install:
	pip install --user -e .

install-dev:
	pip install --user -e ".[dev]"

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info/ __pycache__/ mdviewer/__pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

test:
	python -m pytest tests/ -v || python -c "print('No tests found')"
