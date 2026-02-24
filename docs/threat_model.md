# Basic Threat Model (Phase 0)

## Scope
Local demo platform; threats focus on insecure defaults that could leak data or permit tampering if reused in broader environments.

## Assets
- Training data and generated features.
- Model artifacts and registry metadata.
- Prediction logs and drift reports.
- Service credentials (env vars, webhook URLs).

## Threats (STRIDE-style summary)
- **Spoofing**: unauthenticated local endpoints could be called by unintended clients.
- **Tampering**: model artifacts or feature definitions modified without review.
- **Repudiation**: insufficient logs for model promotion decisions.
- **Information Disclosure**: secrets committed to repo or exposed in logs.
- **Denial of Service**: unbounded request rates on serving API.
- **Elevation of Privilege**: over-permissive container/service defaults.

## Controls (Initial)
- Keep secrets out of git (`.env.example` only).
- Structured logging and promotion decision logging.
- CI checks + required tests prior to merge.
- Health checks and constrained container dependencies.
- Explicit model validation thresholds before Production promotion.

## Future Hardening
- Add API auth (token or mTLS).
- Signed model artifacts and checksum verification.
- Role-based controls for registry stage transitions.
- Centralized secret management.

