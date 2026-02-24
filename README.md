# Production ML Platform (Monorepo)

A portfolio-ready end-to-end MLOps platform demonstrating experiment tracking, feature store usage, model registry promotion, serving, drift detection, and model CI/CD.

## Current Iteration Status

This iteration delivers:
- Phase 0: concise PRD, architecture, data flow, and basic threat model.
- Phase 1: monorepo skeleton, Python tooling (Poetry, pre-commit, lint/test), and initial tests.
- Phase 2: local infrastructure with Docker Compose for Postgres, Redis, MinIO, MLflow, Prometheus, and Grafana (all with health checks).

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

## Quickstart (Current: Tooling + Infra)

```bash
cp .env.example .env
make init
make check
make infra-up
```

### Infra Endpoints
- MLflow: `http://localhost:5001`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Next Iterations

- Phase 3: Feast feature repository definitions + apply/materialize workflows.
- Phase 4+: training, serving, drift, model CI/CD workflows.
