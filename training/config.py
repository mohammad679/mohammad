from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingConfig:
    feast_repo_path: str = os.getenv("FEAST_REPO_PATH", "feature_store/repo")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001")
    mlflow_experiment_name: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "baseline-experiment")
    model_name: str = os.getenv("MODEL_NAME", "breast-cancer-classifier")
    promotion_min_f1: float = float(os.getenv("PROMOTION_MIN_F1", "0.90"))
