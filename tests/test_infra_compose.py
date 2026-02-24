import re
from pathlib import Path


COMPOSE_PATH = Path("infra/docker-compose.yml")


def test_compose_file_exists() -> None:
    assert COMPOSE_PATH.exists()


def test_required_services_present() -> None:
    content = COMPOSE_PATH.read_text()
    for service in ["postgres:", "redis:", "minio:", "mlflow:", "prometheus:", "grafana:"]:
        assert service in content


def test_all_long_running_services_have_healthchecks() -> None:
    content = COMPOSE_PATH.read_text()
    for service in ["postgres", "redis", "minio", "mlflow", "prometheus", "grafana"]:
        pattern = rf"^  {service}:\n(.*?)(?=^  [a-z0-9\-]+:|^volumes:|^networks:|\Z)"
        match = re.search(pattern, content, flags=re.MULTILINE | re.DOTALL)
        assert match, f"Missing block for service {service}"
        assert "healthcheck:" in match.group(1)
