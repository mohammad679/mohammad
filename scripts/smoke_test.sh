#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true

# Basic infra smoke
curl -fsS http://localhost:5001/health >/dev/null
curl -fsS http://localhost:9090/-/healthy >/dev/null
curl -fsS http://localhost:3000/api/health >/dev/null

echo "Smoke checks passed"
