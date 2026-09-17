from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StepType(str, Enum):
    HTTP = "http"
    SCRIPT = "script"
    EMAIL = "email"


class StepCreate(BaseModel):
    name: str
    type: StepType
    config: dict = Field(default_factory=dict)
    position: int
    depends_on: list[str] = Field(default_factory=list)


class StepUpdate(BaseModel):
    name: str | None = None
    type: StepType | None = None
    config: dict | None = None
    position: int | None = None
    depends_on: list[str] | None = None


class StepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    workflow_id: UUID
    name: str
    type: StepType
    config: dict
    position: int
    depends_on: list[str]
    created_at: datetime
    updated_at: datetime
