from __future__ import annotations

import logging
from typing import Any

import mlflow
from feast import FeatureStore
from mlflow import MlflowClient

from serving.config import ServingConfig

FEATURES = [
    "driver_stats_fv:mean_radius",
    "driver_stats_fv:mean_texture",
    "driver_stats_fv:mean_perimeter",
    "driver_stats_fv:mean_area",
]

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self, config: ServingConfig) -> None:
        self.config = config
        self.store = FeatureStore(repo_path=config.feast_repo_path)
        mlflow.set_tracking_uri(config.mlflow_tracking_uri)
        self.client = MlflowClient(tracking_uri=config.mlflow_tracking_uri)
        self._model: Any | None = None
        self._model_version: str = "unknown"

    @property
    def model_version(self) -> str:
        return self._model_version

    def _load_production_model(self) -> Any:
        if self._model is None:
            model_uri = f"models:/{self.config.model_name}/Production"
            self._model = mlflow.pyfunc.load_model(model_uri)
            latest = self.client.get_latest_versions(self.config.model_name, stages=["Production"])
            if latest:
                self._model_version = str(latest[0].version)
            logger.info("Loaded production model", extra={"model_uri": model_uri, "version": self._model_version})
        return self._model

    def fetch_online_features(self, entity_id: int) -> list[float]:
        response = self.store.get_online_features(
            features=FEATURES,
            entity_rows=[{"entity_id": entity_id}],
        ).to_dict()
        values = [response[feature][0] for feature in FEATURES]
        if any(value is None for value in values):
            raise ValueError(f"Missing features for entity_id={entity_id}")
        return [float(value) for value in values]

    def predict(self, entity_id: int) -> int:
        model = self._load_production_model()
        features = self.fetch_online_features(entity_id=entity_id)
        pred = model.predict([features])[0]
        return int(pred)
