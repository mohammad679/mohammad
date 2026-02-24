# Production ML Platform (Monorepo)

A portfolio-ready end-to-end MLOps platform demonstrating experiment tracking, feature store usage, model registry promotion, serving, drift detection, and model CI/CD.

## Current Iteration Status

This iteration delivers:
- Phase 0: concise PRD, architecture, data flow, and basic threat model.
- Phase 1: monorepo skeleton, Python tooling (Poetry, pre-commit, lint/test), and initial tests.
- Phase 2: local infrastructure with Docker Compose for Postgres, Redis, MinIO, MLflow, Prometheus, and Grafana (all with health checks).
- Phase 3: Feast feature repository with Postgres offline source + Redis online store and materialization commands.

## Target Repository Layout

```text
.
├── infra/
├── feature_store/
├── training/
├── serving/
├── drift/
├── shared/
├── tests/
├── .github/workflows/
├── docs/
├── scripts/
├── pyproject.toml
├── Makefile
└── README.md
```

## Quickstart (Current: Tooling + Infra + Feature Store)

```bash
cp .env.example .env
make init
make check
make infra-up
make feast-bootstrap
make feast-apply
make feast-materialize
```

### Infra Endpoints
- MLflow: `http://localhost:5001`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Feature Store Notes
- Feast repo path: `feature_store/repo`.
- Offline source table: `driver_stats` in Postgres.
- Bootstrap script uses sklearn breast cancer dataset and writes deterministic feature columns.

## Next Iterations

- Phase 4: training pipeline with MLflow logging, registration, and promotion gate.
- Phase 5+: serving, drift, model CI/CD workflows.
