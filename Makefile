PYTHON = python3
RUFF = ruff
PYTEST = pytest
COVERAGE = --cov=src --cov-report=term-missing

.PHONY: all
all: test

.PHONY: test
test:
# uv run pytest

.PHONY: cov
cov:
# uv run pytest ${COVERAGE}

.PHONY: lint
lint:
# uv run ruff check src
# uv run mypy src

.PHONY: install
install:
# uv sync

.PHONY: run
run:
# run python -m src.pybites_pdc_snipster.main
