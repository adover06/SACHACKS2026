from pydantic import BaseModel, Field
from uuid import uuid4


class IdentifiedItem(BaseModel):
    name: str
    confidence: float = Field(ge=0.0, le=1.0)
    source: str = "ASUCD Pantry"


class ScanResponse(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    identified_items: list[IdentifiedItem]
    suggested_filters: list[str]
