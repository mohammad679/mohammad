# Phase 0 PRD — Production ML Platform

## 1) Product Goal
Build a local-first, production-style ML platform monorepo that demonstrates an end-to-end ML lifecycle:
- experimentation,
- feature management,
- training and registry promotion,
- online inference,
- drift monitoring,
- CI/CD automation.

## 2) Target Users
- Hiring managers and interviewers evaluating MLOps depth.
- Engineers wanting a runnable reference architecture for local ML platforms.

## 3) In-Scope Capabilities
1. Experiment Tracking via MLflow.
2. Feature Store via Feast (offline Postgres + online Redis).
3. Model Registry and stage promotion in MLflow.
4. Reproducible training pipeline using Feast features.
5. FastAPI serving API with online feature fetch and Production model loading.
6. Drift job with JSON + HTML reports, MLflow logging, and alert stub.
7. CI/CD (lint/test/build/integration/deploy-smoke).
8. Observability with Prometheus + Grafana.

## 4) Non-Goals
- Cloud provider-specific production deployment.
- Large-scale distributed training.
- Complex authN/authZ beyond local safety defaults.

## 5) Success Criteria
- Full demo path runs locally via documented commands.
- Model can be trained, registered, promoted, and served.
- Drift report generated after predictions are produced.
- CI validates code and containerized integration path.

## 6) Data + Model Defaults
- Dataset: `sklearn` built-in dataset (fast, no external download).
- Baseline model: tree-based classifier (fast and interpretable).
- Threshold gates for promotion and drift alerts are configurable via env.

## 7) Risks and Mitigations
- **Version incompatibility** across MLflow/Feast: pin versions and add smoke checks.
- **Infra startup order** issues: compose health checks and dependency conditions.
- **Schema drift** in features: typed shared schemas + validation tests.

