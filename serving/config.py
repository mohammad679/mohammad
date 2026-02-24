from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ServingConfig:
    feast_repo_path: str = os.getenv("FEAST_REPO_PATH", "feature_store/repo")
    model_name: str = os.getenv("MODEL_NAME", "breast-cancer-classifier")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001")
    host: str = os.getenv("SERVING_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVING_PORT", "8000"))
