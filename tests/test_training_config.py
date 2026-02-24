from training.config import TrainingConfig


def test_training_config_defaults() -> None:
    cfg = TrainingConfig()
    assert cfg.feast_repo_path == "feature_store/repo"
    assert cfg.model_name == "breast-cancer-classifier"
    assert cfg.promotion_min_f1 > 0
