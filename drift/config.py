from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DriftConfig:
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001")
    mlflow_experiment_name: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "baseline-experiment")
    drift_threshold: float = float(os.getenv("DRIFT_THRESHOLD", "0.20"))
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    baseline_path: str = os.getenv("DRIFT_BASELINE_PATH", "drift/baseline/baseline_features.csv")
    recent_path: str = os.getenv("DRIFT_RECENT_PATH", "drift/baseline/recent_features.csv")
    report_dir: str = os.getenv("DRIFT_REPORT_DIR", "drift/reports")
