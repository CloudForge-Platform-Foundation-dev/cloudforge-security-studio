"""API routes of Security Studio."""
from collections import Counter
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError

from src.auth import Principal, require_security_read, require_security_write
from src.models.schemas import (
    FINDING_EVENT_TYPE,
    CanonicalEvent,
    EventAccepted,
    Finding,
    FindingPayload,
    FindingsResponse,
    Severity,
)
from src.store import EventStore

router = APIRouter()
_store = EventStore()


def get_store() -> EventStore:
    """Dependency provider — tests override this with a fresh store."""
    return _store


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/events", response_model=EventAccepted, status_code=202)
def ingest_event(
    event: CanonicalEvent,
    principal: Principal = Depends(require_security_write),
    store: EventStore = Depends(get_store),
) -> EventAccepted:
    finding = None
    if event.eventType == FINDING_EVENT_TYPE:
        try:
            payload = FindingPayload.model_validate(event.payload)
        except ValidationError as exc:
            problems = "; ".join(
                f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()
            )
            raise HTTPException(status_code=422, detail=f"Invalid {FINDING_EVENT_TYPE} payload: {problems}") from None
        finding = Finding(
            eventId=event.eventId,
            source=event.source,
            severity=payload.severity,
            title=payload.title,
            resource=payload.resource,
            description=payload.description,
            eventTimestamp=event.timestamp,
            receivedAt=datetime.now(timezone.utc),
            reportedBy=principal.sub,
        )
    if not store.add(event, finding):
        raise HTTPException(status_code=409, detail="Event already received")
    return EventAccepted(eventId=event.eventId, findingCreated=finding is not None)


@router.get("/findings", response_model=FindingsResponse)
def list_findings(
    severity: Severity | None = None,
    limit: int = Query(100, ge=1, le=500),
    principal: Principal = Depends(require_security_read),
    store: EventStore = Depends(get_store),
) -> FindingsResponse:
    matching = store.findings(severity)
    counts = Counter(f.severity.value for f in matching)
    return FindingsResponse(total=len(matching), countsBySeverity=dict(counts), findings=matching[:limit])
