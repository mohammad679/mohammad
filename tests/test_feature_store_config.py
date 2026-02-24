from pathlib import Path


def test_feature_store_yaml_structure() -> None:
    content = Path("feature_store/repo/feature_store.yaml").read_text()
    assert "project: production_ml_platform" in content
    assert "offline_store:" in content
    assert "type: postgres" in content
    assert "online_store:" in content
    assert "type: redis" in content


def test_feature_definition_contains_expected_fields() -> None:
    feature_file = Path("feature_store/repo/features/driver_stats.py").read_text()
    for field_name in [
        "mean_radius",
        "mean_texture",
        "mean_perimeter",
        "mean_area",
        "target",
    ]:
        assert f'name="{field_name}"' in feature_file


def test_bootstrap_script_targets_driver_stats_table() -> None:
    script = Path("feature_store/scripts/bootstrap_offline_store.py").read_text()
    assert 'to_sql("driver_stats"' in script
