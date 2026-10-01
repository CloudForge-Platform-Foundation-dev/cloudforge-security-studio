"""In-memory event/finding store (MVP — see docs/adr/001). Data is lost on restart."""
from threading import Lock
from uuid import UUID

from src.models.schemas import CanonicalEvent, Finding, Severity


class EventStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._events: dict[UUID, CanonicalEvent] = {}
        self._findings: list[Finding] = []

    def add(self, event: CanonicalEvent, finding: Finding | None = None) -> bool:
        """Store the event (+ finding). Returns False if eventId was already received."""
        with self._lock:
            if event.eventId in self._events:
                return False
            self._events[event.eventId] = event
            if finding is not None:
                self._findings.append(finding)
            return True

    def findings(self, severity: Severity | None = None) -> list[Finding]:
        """Newest first, optionally filtered by severity."""
        with self._lock:
            return [f for f in reversed(self._findings) if severity is None or f.severity == severity]

    def event_count(self) -> int:
        with self._lock:
            return len(self._events)
