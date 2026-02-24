from drift.config import DriftConfig


def test_drift_config_defaults() -> None:
    cfg = DriftConfig()
    assert cfg.drift_threshold > 0
    assert cfg.baseline_path.endswith("baseline_features.csv")
    assert cfg.recent_path.endswith("recent_features.csv")
