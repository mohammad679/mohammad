from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    entity_id: int = Field(..., ge=0, description="Entity identifier for feature lookup")


class PredictResponse(BaseModel):
    entity_id: int
    prediction: int
    model_stage: str = "Production"
