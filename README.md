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

## Quickstart (Current: Tooling + Infra + Feature Store + Training + Serving)

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
```

### Serving Endpoints
- API docs: `http://localhost:8000/docs`
- Health: `GET http://localhost:8000/health`
- Metrics: `GET http://localhost:8000/metrics`
- Predict: `POST http://localhost:8000/predict` with body `{"entity_id": 1}`

### Infra Endpoints
- MLflow: `http://localhost:5001`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Training Notes
- Training script fetches historical features from Feast, trains logistic regression, logs metrics/params to MLflow, and registers model name from `MODEL_NAME`.
- Promotion script evaluates latest model run's F1 metric against `PROMOTION_MIN_F1` and promotes to `Production` when threshold passes.

## Serving Notes
- Serving loads model URI `models:/<MODEL_NAME>/Production` from MLflow Registry.
- Serving fetches online features from Feast Redis store and exposes Prometheus metrics for request count and latency.

## Next Iterations

- Phase 6: drift detection job, report artifacts, and alerting stub.
- Phase 7+: model CI/CD and deploy/smoke workflows.
