# Architecture and Data Flow (Phase 0)

## Components
- **infra/**: Docker Compose and configs for Postgres, Redis, MLflow, Prometheus, Grafana.
- **feature_store/**: Feast repo and feature definitions.
- **training/**: data prep, Feast retrieval, training, validation, registry operations.
- **serving/**: FastAPI inference service using Feast online features and MLflow Production model.
- **drift/**: scheduled drift calculations, report generation, and alert stubs.
- **shared/**: common schemas, logging, and config helpers.

## Data Flow
1. Raw/entity records are prepared for feature generation.
2. Feast manages offline features in Postgres and materializes to Redis online store.
3. Training job pulls point-in-time features, trains model, logs to MLflow, registers model.
4. Promotion gate validates metrics; qualifying model promoted to Production.
5. Serving API receives request, fetches online features from Feast, loads Production model, returns prediction.
6. Prediction logs feed drift job; job compares against baseline and emits reports + MLflow metrics.
7. Prometheus scrapes service/job metrics; Grafana visualizes health and performance.

## Operational Defaults
- Local-first execution with Docker Compose profiles.
- `.env` based configuration (templated in `.env.example`).
- Health endpoints for all long-running services.

