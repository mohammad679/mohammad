from __future__ import annotations

import logging
import time

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from serving.config import ServingConfig
from serving.service import PredictionService
from shared.schemas import PredictRequest, PredictResponse

logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter("serving_requests_total", "Total prediction requests")
REQUEST_LATENCY = Histogram("serving_request_latency_seconds", "Latency of prediction requests")

config = ServingConfig()
service = PredictionService(config=config)
app = FastAPI(title="Production ML Platform Serving", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    REQUEST_COUNT.inc()
    start = time.perf_counter()
    try:
        prediction = service.predict(entity_id=payload.entity_id)
        return PredictResponse(
            entity_id=payload.entity_id,
            prediction=prediction,
            model_stage="Production",
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Prediction error: {exc}") from exc
    finally:
        REQUEST_LATENCY.observe(time.perf_counter() - start)
