from pathlib import Path


def test_ci_workflow_has_required_jobs() -> None:
    content = Path('.github/workflows/ci.yml').read_text()
    assert 'lint-test:' in content
    assert 'docker-build-integration:' in content
    assert 'deploy-smoke-main:' in content


def test_model_promotion_workflow_exists() -> None:
    content = Path('.github/workflows/model-promotion.yml').read_text()
    assert 'name: model-promotion-gate' in content
    assert 'promote-if-valid:' in content


def test_integration_scripts_exist() -> None:
    assert Path('scripts/integration_test.sh').exists()
    assert Path('scripts/smoke_test.sh').exists()
