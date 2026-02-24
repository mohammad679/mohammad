#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true

docker compose --env-file .env -f infra/docker-compose.yml up -d postgres redis minio create-bucket mlflow

# Wait for MLflow health endpoint
for i in {1..40}; do
  if curl -fsS http://localhost:5001/health >/dev/null; then
    echo "MLflow is healthy"
    break
  fi
  sleep 3
  if [[ "$i" == "40" ]]; then
    echo "MLflow failed to become healthy"
    exit 1
  fi
done

docker compose --env-file .env -f infra/docker-compose.yml down -v
