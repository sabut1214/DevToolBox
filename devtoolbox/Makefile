.PHONY: install dev test lint clean

install:
	pip install -e .

dev:
	pip install -e .[dev]

test:
	pytest

lint:
	ruff check .

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ *.egg-info .dist .build
