from __future__ import annotations

import mlflow
from mlflow import MlflowClient

from training.config import TrainingConfig
from training.validation import should_promote_model


def promote_latest_version_if_valid(config: TrainingConfig, metric_name: str = "f1") -> dict[str, str | float | bool]:
    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    client = MlflowClient(tracking_uri=config.mlflow_tracking_uri)

    latest_versions = client.get_latest_versions(config.model_name)
    if not latest_versions:
        raise RuntimeError(f"No versions found for model '{config.model_name}'.")

    candidate = max(latest_versions, key=lambda item: int(item.version))
    run = client.get_run(candidate.run_id)
    f1_value = float(run.data.metrics.get(metric_name, 0.0))

    passed = should_promote_model(f1_score_value=f1_value, threshold=config.promotion_min_f1)

    if passed:
        client.transition_model_version_stage(
            name=config.model_name,
            version=candidate.version,
            stage="Production",
            archive_existing_versions=True,
        )

    return {
        "model_name": config.model_name,
        "version": candidate.version,
        "metric_name": metric_name,
        "metric_value": f1_value,
        "threshold": config.promotion_min_f1,
        "promoted": passed,
    }
