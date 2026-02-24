from serving.config import ServingConfig


def test_serving_config_defaults() -> None:
    cfg = ServingConfig()
    assert cfg.feast_repo_path == "feature_store/repo"
    assert cfg.model_name == "breast-cancer-classifier"
    assert cfg.port == 8000
