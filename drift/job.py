from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import mlflow
import pandas as pd

from drift.alert import trigger_alert
from drift.config import DriftConfig
from drift.metrics import psi

FEATURES = ["mean_radius", "mean_texture", "mean_perimeter", "mean_area"]


def compute_drift(config: DriftConfig) -> dict[str, object]:
    baseline = pd.read_csv(config.baseline_path)
    recent = pd.read_csv(config.recent_path)

    feature_psi = {feature: psi(baseline[feature], recent[feature]) for feature in FEATURES}
    max_psi = float(max(feature_psi.values())) if feature_psi else 0.0
    drift_detected = max_psi >= config.drift_threshold

    result = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "threshold": config.drift_threshold,
        "max_psi": max_psi,
        "drift_detected": drift_detected,
        "feature_psi": feature_psi,
    }

    Path(config.report_dir).mkdir(parents=True, exist_ok=True)
    json_path = Path(config.report_dir) / "drift_report.json"
    html_path = Path(config.report_dir) / "drift_report.html"

    json_path.write_text(json.dumps(result, indent=2))

    rows = "".join([f"<tr><td>{k}</td><td>{v:.6f}</td></tr>" for k, v in feature_psi.items()])
    html = f"""
    <html><body>
    <h1>Drift Report</h1>
    <p>Threshold: {config.drift_threshold}</p>
    <p>Max PSI: {max_psi:.6f}</p>
    <p>Drift detected: {drift_detected}</p>
    <table border='1'><tr><th>Feature</th><th>PSI</th></tr>{rows}</table>
    </body></html>
    """
    html_path.write_text(html.strip())

    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    mlflow.set_experiment(config.mlflow_experiment_name)
    with mlflow.start_run(run_name="drift-detection"):
        mlflow.log_params({"drift_threshold": config.drift_threshold})
        mlflow.log_metric("drift_max_psi", max_psi)
        for feature, value in feature_psi.items():
            mlflow.log_metric(f"drift_psi_{feature}", float(value))
        mlflow.log_artifact(str(json_path))
        mlflow.log_artifact(str(html_path))

    if drift_detected:
        trigger_alert(
            message=f"Drift threshold exceeded: max_psi={max_psi:.6f} >= {config.drift_threshold}",
            webhook_url=config.slack_webhook_url,
        )

    return result
