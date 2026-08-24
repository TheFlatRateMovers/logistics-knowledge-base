#!/usr/bin/env python3
"""Authoritative projection of canonical logistics events into current state."""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "generated"
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_MACHINE_FILE = ROOT / "protocol" / "logistics-state-machine.json"


class CurrentStateStore:
    """Current operational truth derived from immutable canonical events."""

    def __init__(self):
        self.jobs = {}
        self.customers = {}
        self.shipments = {}
        self.vehicles = {}
        self.crews = {}
        self.locations = {}
        self.equipment = {}
        self.state_graph = self._load_state_graph()

    @staticmethod
    def _load_state_graph():
        with STATE_MACHINE_FILE.open("r", encoding="utf-8") as handle:
            machine = json.load(handle)
        return {
            item["state"]: set(item.get("nextStates", []))
            for item in machine["states"]
        }

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()

    def upsert(self, store, entity_id, data):
        current = store.setdefault(entity_id, {})
        current.update(data)
        current["lastUpdated"] = self._now()
        return current

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def apply_event(self, event):
        event_type = event.get("eventType")
        entity_id = event.get("entityId")
        entity_type = event.get("entityType")
        transition = event.get("stateTransition", {})
        previous = transition.get("previousState")
        new = transition.get("newState")

        if not event_type or not entity_id or not entity_type:
            raise ValueError("eventType, entityId, and entityType are required")

        if previous and new and previous != new and new not in self.state_graph.get(previous, set()):
            raise ValueError(f"Illegal state transition: {previous} -> {new} for {event_type}")

        payload = event.get("payload", {})
        projection = {
            "entityType": entity_type,
            "status": new or payload.get("status"),
            "lastEventType": event_type,
            "lastEventId": event.get("eventId"),
            "lastEventTimestamp": event.get("eventTimestamp"),
            "correlationId": event.get("correlationId"),
        }
        projection.update(payload)

        stores = {
            "job": self.jobs,
            "customer": self.customers,
            "shipment": self.shipments,
            "vehicle": self.vehicles,
            "crew_member": self.crews,
            "location": self.locations,
            "equipment": self.equipment,
        }
        store = stores.get(entity_type, self.jobs if entity_type == "job" else None)
        if store is not None:
            self.upsert(store, entity_id, projection)

        # Relationship projections carried by assignment events.
        if event_type == "VEHICLE_ASSIGNED" and entity_type == "job":
            vehicle_id = payload.get("vehicleId") or payload.get("vehicle_id")
            if vehicle_id:
                self.jobs[entity_id].setdefault("vehicleIds", [])
                if vehicle_id not in self.jobs[entity_id]["vehicleIds"]:
                    self.jobs[entity_id]["vehicleIds"].append(vehicle_id)

        if event_type == "CREW_ASSIGNED" and entity_type == "job":
            crew_id = payload.get("crewId") or payload.get("crew_id")
            if crew_id:
                self.jobs[entity_id].setdefault("crewIds", [])
                if crew_id not in self.jobs[entity_id]["crewIds"]:
                    self.jobs[entity_id]["crewIds"].append(crew_id)

        return self.jobs.get(entity_id) if entity_type == "job" else projection

    def save_state(self):
        exports = {
            "job-state.json": self.jobs,
            "customer-state.json": self.customers,
            "shipment-state.json": self.shipments,
            "vehicle-state.json": self.vehicles,
            "crew-state.json": self.crews,
            "equipment-state.json": self.equipment,
            "location-state.json": self.locations,
        }
        for filename, data in exports.items():
            with (STATE_DIR / filename).open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, ensure_ascii=False)

    def system_snapshot(self):
        return {
            "jobs": len(self.jobs),
            "customers": len(self.customers),
            "shipments": len(self.shipments),
            "vehicles": len(self.vehicles),
            "crews": len(self.crews),
            "equipment": len(self.equipment),
            "locations": len(self.locations),
            "generated": self._now(),
        }


STATE_STORE = CurrentStateStore()
