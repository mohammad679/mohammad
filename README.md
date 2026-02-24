# Production ML Platform (Monorepo)

A portfolio-ready end-to-end MLOps platform demonstrating experiment tracking, feature store usage, model registry promotion, serving, drift detection, and model CI/CD.

## Current Iteration Status

This iteration delivers:
- Phase 0: concise PRD, architecture, data flow, and basic threat model.
- Phase 1: monorepo skeleton, Python tooling (Poetry, pre-commit, lint/test), and initial tests.

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

## Architecture (Target)

```text
           +------------------+
           |   Data Sources   |
           +---------+--------+
                     |
                     v
             +-------+-------+
             |   Feast Repo  |
             | Offline: PG   |
             | Online: Redis |
             +---+-------+---+
                 |       |
      training   |       | serving lookup
                 v       v
         +-------+-------+---------+
         |  Training Pipeline       |
         |  sklearn + MLflow        |
         +-------+---------+--------+
                 |         |
            metrics/artif. | register/promote
                 v         v
            +----+---------+----+
            |   MLflow Tracking  |
            | + Model Registry   |
            +----+---------+----+
                 |         |
                 | load prod model
                 v         v
         +-------+---------+--------+
         | FastAPI Serving Service  |
         | /predict /health /metrics|
         +-------+---------+--------+
                 |
                 v
         +-------+---------+
         | Drift Job       |
         | reports + alert |
         +-----------------+

 Observability: Prometheus + Grafana scrape app/infra metrics
```

## Quickstart (Tooling Only, current phase)

```bash
make init
make check
```

## Next Iterations

- Phase 2: Docker Compose infrastructure (Postgres, Redis, MLflow, MinIO optional, Prometheus, Grafana).
- Phase 3+: Feast definitions, training, serving, drift, CI/CD workflows.

