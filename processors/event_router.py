#!/usr/bin/env python3
"""Canonical logistics event router."""

import json
from pathlib import Path

try:
    from processors.schema_validator import validate_event
except ModuleNotFoundError:
    from schema_validator import validate_event

ROOT = Path(__file__).resolve().parents[1]
EVENT_QUEUE = ROOT / "event-stream"
PROCESSED = ROOT / "processed-events"


class EventRouter:
    """Routes only validated canonical event types to implemented handlers."""

    def __init__(self):
        self.handlers = {
            "JOB_CREATED": self.job_created,
            "ESTIMATE_GENERATED": self.estimate_generated,
            "VEHICLE_ASSIGNED": self.vehicle_assigned,
            "CREW_ASSIGNED": self.crew_assigned,
            "PICKUP_STARTED": self.pickup_started,
            "IN_TRANSIT": self.in_transit,
            "DELIVERY_COMPLETED": self.delivery_completed,
        }

    def route(self, event):
        validate_event(event)
        event_type = event["eventType"]
        handler = self.handlers.get(event_type)
        if not handler:
            raise ValueError(f"Event {event_type} is protocol-defined but has no router implementation")
        return handler(event)

    def _processed(self, event):
        return {"status": "processed", "eventType": event["eventType"], "eventId": event["eventId"]}

    def job_created(self, event):
        return self._processed(event)

    def estimate_generated(self, event):
        return self._processed(event)

    def vehicle_assigned(self, event):
        return self._processed(event)

    def crew_assigned(self, event):
        return self._processed(event)

    def pickup_started(self, event):
        return self._processed(event)

    def in_transit(self, event):
        return self._processed(event)

    def delivery_completed(self, event):
        return self._processed(event)


def process_file(filepath: Path, router: EventRouter):
    with filepath.open("r", encoding="utf-8") as handle:
        event = json.load(handle)
    result = router.route(event)
    destination = PROCESSED / filepath.name
    PROCESSED.mkdir(parents=True, exist_ok=True)
    filepath.rename(destination)
    return result


def run_event_stream():
    EVENT_QUEUE.mkdir(parents=True, exist_ok=True)
    router = EventRouter()
    for file in sorted(EVENT_QUEUE.glob("*.json")):
        try:
            process_file(file, router)
        except Exception as exc:
            print(f"ERROR {file.name}: {exc}")


if __name__ == "__main__":
    run_event_stream()
