from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone

import mlflow
import pandas as pd
from feast import FeatureStore
from mlflow.models.signature import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from training.config import TrainingConfig


FEATURE_COLUMNS = [
    "mean_radius",
    "mean_texture",
    "mean_perimeter",
    "mean_area",
]
TARGET_COLUMN = "target"


def build_entity_dataframe(entity_count: int) -> pd.DataFrame:
    now = datetime.now(tz=timezone.utc)
    return pd.DataFrame(
        {
            "entity_id": list(range(entity_count)),
            "event_timestamp": [now] * entity_count,
        }
    )


def fetch_training_frame(config: TrainingConfig, entity_count: int = 569) -> pd.DataFrame:
    store = FeatureStore(repo_path=config.feast_repo_path)
    entity_df = build_entity_dataframe(entity_count=entity_count)
    retrieval = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "driver_stats_fv:mean_radius",
            "driver_stats_fv:mean_texture",
            "driver_stats_fv:mean_perimeter",
            "driver_stats_fv:mean_area",
            "driver_stats_fv:target",
        ],
    )
    return retrieval.to_df().dropna().copy()


def train_and_log(config: TrainingConfig) -> dict[str, float | str | int]:
    frame = fetch_training_frame(config)

    x_train, x_test, y_train, y_test = train_test_split(
        frame[FEATURE_COLUMNS], frame[TARGET_COLUMN], test_size=0.2, random_state=42, stratify=frame[TARGET_COLUMN]
    )

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions)),
        "recall": float(recall_score(y_test, predictions)),
        "f1": float(f1_score(y_test, predictions)),
    }

    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    mlflow.set_experiment(config.mlflow_experiment_name)

    with mlflow.start_run(run_name="baseline-logistic-regression") as run:
        mlflow.log_params(
            {
                "model_type": "LogisticRegression",
                "max_iter": 1000,
                "random_state": 42,
                "test_size": 0.2,
                **asdict(config),
            }
        )
        mlflow.log_metrics(metrics)

        signature = infer_signature(x_train, model.predict(x_train))
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            input_example=x_train.head(2),
            registered_model_name=config.model_name,
        )

        return {
            "run_id": run.info.run_id,
            "registered_model_name": config.model_name,
            "model_uri": model_info.model_uri,
            "accuracy": metrics["accuracy"],
            "f1": metrics["f1"],
        }
