from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str
    version: str
    environment: str
    timestamp: datetime


class DatabaseHealthResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    database: str = Field(description="Database engine and server version, when reachable.")
    latency_ms: float | None = None
    detail: str | None = None
