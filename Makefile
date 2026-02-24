SHELL := /bin/bash

.PHONY: install format lint test check init

install:
	poetry install

format:
	poetry run ruff format .
	poetry run black .

lint:
	poetry run ruff check .
	poetry run black --check .
	poetry run mypy shared

test:
	poetry run pytest

check: lint test

init:
	poetry install
	poetry run pre-commit install
