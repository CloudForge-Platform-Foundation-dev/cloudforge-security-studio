"""Models. CanonicalEvent mirrors Foundation schemas/canonical/event.schema.json."""
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

FINDING_EVENT_TYPE = "Finding.Created"
EVENT_TYPE_PATTERN = r"^[A-Z][a-zA-Z0-9]+\.(Created|Updated|Deleted|Action|Failed)$"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class EventMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")
    schemaVersion: str | None = Field(None, pattern=r"^v\d+\.\d+$")
    traceId: str | None = None

    @model_validator(mode="after")
    def _extras_are_strings(self):
        for key, value in (self.model_extra or {}).items():
            if not isinstance(value, str):
                raise ValueError(f"metadata.{key} must be a string")
        return self


class CanonicalEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")  # schema: additionalProperties=false
    eventId: UUID
    eventType: str = Field(..., pattern=EVENT_TYPE_PATTERN)
    source: str = Field(..., min_length=1)  # the EMITTING studio, e.g. "ingest-studio"
    timestamp: datetime
    correlationId: UUID | None = None
    causationId: UUID | None = None
    payload: dict[str, Any]
    metadata: EventMetadata | None = None


class FindingPayload(BaseModel):
    """Payload required when eventType == Finding.Created."""
    model_config = ConfigDict(extra="allow")
    severity: Severity
    title: str = Field(..., min_length=1)
    resource: str | None = None
    description: str | None = None


class Finding(BaseModel):
    eventId: UUID
    source: str
    severity: Severity
    title: str
    resource: str | None = None
    description: str | None = None
    eventTimestamp: datetime
    receivedAt: datetime
    reportedBy: str


class EventAccepted(BaseModel):
    eventId: UUID
    findingCreated: bool


class FindingsResponse(BaseModel):
    total: int
    countsBySeverity: dict[str, int]
    findings: list[Finding]
