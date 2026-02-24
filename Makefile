SHELL := /bin/bash

.PHONY: install format lint test check init infra-up infra-down infra-logs feast-bootstrap feast-apply feast-materialize train-run model-promote serve-run drift-run

install:
	poetry install

format:
	poetry run ruff format .
	poetry run black .

lint:
	poetry run ruff check .
	poetry run black --check .
	poetry run mypy shared training serving drift

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

feast-bootstrap:
	poetry run python feature_store/scripts/bootstrap_offline_store.py

feast-apply:
	cd feature_store/repo && poetry run feast apply

feast-materialize:
	cd feature_store/repo && poetry run feast materialize-incremental $$(date -u +%Y-%m-%dT%H:%M:%S)

train-run:
	poetry run python training/scripts/run_training.py

model-promote:
	poetry run python training/scripts/promote_model.py

serve-run:
	poetry run python -m serving.main

drift-run:
	poetry run python drift/scripts/run_drift.py
