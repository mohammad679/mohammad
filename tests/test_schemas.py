import pytest
from pydantic import ValidationError

from shared.schemas import PredictRequest, PredictResponse


def test_predict_request_valid() -> None:
    req = PredictRequest(entity_id=7)
    assert req.entity_id == 7


def test_predict_request_rejects_negative_entity_id() -> None:
    with pytest.raises(ValidationError):
        PredictRequest(entity_id=-1)


def test_predict_response_defaults_stage() -> None:
    response = PredictResponse(entity_id=7, prediction=1)
    assert response.model_stage == "Production"
