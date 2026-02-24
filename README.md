# Production ML Platform (Monorepo)

A portfolio-ready end-to-end MLOps platform demonstrating experiment tracking, feature store usage, model registry promotion, serving, drift detection, and model CI/CD.

## Current Iteration Status

This iteration delivers:
- Phase 0: concise PRD, architecture, data flow, and basic threat model.
- Phase 1: monorepo skeleton, Python tooling (Poetry, pre-commit, lint/test), and initial tests.
- Phase 2: local infrastructure with Docker Compose for Postgres, Redis, MinIO, MLflow, Prometheus, and Grafana (all with health checks).
- Phase 3: Feast feature repository with Postgres offline source + Redis online store and materialization commands.
- Phase 4: reproducible training pipeline using Feast historical features, MLflow run logging, model registration, and promotion gating.
- Phase 5: FastAPI serving API fetching Feast online features and loading the Production model from MLflow registry.
- Phase 6: drift detection job with PSI metrics, JSON/HTML reports, MLflow logging, and alert stub.

## Quickstart (Current: Tooling + Infra + Feature Store + Training + Serving + Drift)

```bash
cp .env.example .env
make init
make check
make infra-up
make feast-bootstrap
make feast-apply
make feast-materialize
make train-run
make model-promote
make serve-run
make drift-run
```

### Serving Endpoints
- API docs: `http://localhost:8000/docs`
- Health: `GET http://localhost:8000/health`
- Metrics: `GET http://localhost:8000/metrics`
- Predict: `POST http://localhost:8000/predict` with body `{"entity_id": 1}`

### Drift Outputs
- JSON report: `drift/reports/drift_report.json`
- HTML report: `drift/reports/drift_report.html`

## Next Iterations

- Phase 7: model CI/CD workflows (lint/test/build/integration/deploy-smoke).
- Phase 8: polish docs, dashboards, and demo script.
