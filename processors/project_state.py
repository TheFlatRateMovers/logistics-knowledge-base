#!/usr/bin/env python3
"""Project canonical logistics events into current operational state."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "events-data"
OUTPUT_DIR = ROOT / "generated"


def load_events() -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not EVENT_DIR.exists():
        return events
    for path in sorted(EVENT_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        events.extend(data if isinstance(data, list) else [data])
    return sorted(events, key=lambda event: event.get("eventTimestamp", ""))


class ProjectionStore:
    def __init__(self) -> None:
        self.jobs: dict[str, dict[str, Any]] = {}
        self.customers: dict[str, dict[str, Any]] = {}
        self.shipments: dict[str, dict[str, Any]] = {}
        self.vehicles: dict[str, dict[str, Any]] = {}
        self.crews: dict[str, dict[str, Any]] = {}
        self.equipment: dict[str, dict[str, Any]] = {}


def process_event(event: dict[str, Any], state: ProjectionStore) -> None:
    event_type = event.get("eventType")
    payload = event.get("payload") or {}
    entity_id = str(event.get("entityId") or payload.get("jobId") or "")
    if event_type == "JOB_CREATED":
        state.jobs[entity_id] = {"jobId": entity_id, "status": "CREATED", "createdAt": event.get("eventTimestamp"), "payload": payload}
    elif event_type == "ESTIMATE_GENERATED" and entity_id in state.jobs:
        state.jobs[entity_id].update({"status": "QUOTED", "estimate": payload})
    elif event_type == "VEHICLE_ASSIGNED":
        vehicle_id = str(payload.get("vehicleId") or entity_id)
        state.vehicles[vehicle_id] = {"vehicleId": vehicle_id, "status": "ASSIGNED", "jobId": entity_id}
        if entity_id in state.jobs:
            state.jobs[entity_id].setdefault("vehicleIds", []).append(vehicle_id)
    elif event_type == "CREW_ASSIGNED":
        crew_id = str(payload.get("crewId") or entity_id)
        state.crews[crew_id] = {"crewId": crew_id, "status": "ASSIGNED", "jobId": entity_id}
        if entity_id in state.jobs:
            state.jobs[entity_id].setdefault("crewIds", []).append(crew_id)
    elif event_type in {"PICKUP_STARTED", "IN_TRANSIT", "DELIVERY_COMPLETED"} and entity_id in state.jobs:
        state.jobs[entity_id]["status"] = event_type
        state.jobs[entity_id]["lastEventTimestamp"] = event.get("eventTimestamp")


def export_state(state: ProjectionStore) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    outputs = {
        "job-state.json": state.jobs,
        "customer-state.json": state.customers,
        "shipment-state.json": state.shipments,
        "vehicle-state.json": state.vehicles,
        "crew-state.json": state.crews,
        "equipment-state.json": state.equipment,
        "dispatch-dashboard.json": state.jobs,
        "ai-agent-state.json": {"jobs": state.jobs, "vehicles": state.vehicles, "crews": state.crews},
        "current-state.json": {"generatedAt": generated_at, "jobs": len(state.jobs), "vehicles": len(state.vehicles), "crews": len(state.crews), "shipments": len(state.shipments)},
    }
    for filename, data in outputs.items():
        (OUTPUT_DIR / filename).write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    state = ProjectionStore()
    for event in load_events():
        process_event(event, state)
    export_state(state)
    print("State projection complete")


if __name__ == "__main__":
    main()
