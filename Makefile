SHELL := /bin/bash

.PHONY: install format lint test check init infra-up infra-down infra-logs

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

infra-up:
	docker compose --env-file .env -f infra/docker-compose.yml up -d

infra-down:
	docker compose --env-file .env -f infra/docker-compose.yml down -v

infra-logs:
	docker compose --env-file .env -f infra/docker-compose.yml logs -f --tail=100
