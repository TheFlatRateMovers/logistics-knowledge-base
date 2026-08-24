from typing import Dict, Any


class LiveEventGraphUpdater:
    """Apply canonical logistics events to the in-memory GraphRAG graph."""

    def __init__(self, graph_store: Dict[str, Any]):
        self.graph = graph_store

    def process_event(self, event: Dict[str, Any]):
        event_type = event.get("eventType") or event.get("event_type")
        if event_type == "JOB_CREATED":
            self.handle_job_created(event)
        elif event_type == "VEHICLE_ASSIGNED":
            self.handle_vehicle_assigned(event)
        elif event_type == "CREW_ASSIGNED":
            self.handle_crew_assigned(event)
        elif event_type == "DELIVERY_COMPLETED":
            self.handle_delivery_completed(event)
        else:
            # Unknown events remain valid protocol events; they are simply not
            # projected until a graph handler is registered for them.
            return {"status": "accepted", "eventType": event_type, "projected": False}
        return {"status": "projected", "eventType": event_type, "projected": True}

    @staticmethod
    def _job_id(event):
        return event.get("entityId") or event.get("job_id") or event.get("payload", {}).get("jobId")

    def handle_job_created(self, event):
        job_id = self._job_id(event)
        self.graph["nodes"].append({
            "id": job_id,
            "type": "Job",
            "properties": event.get("payload", {})
        })
        self.graph["edges"].append({
            "source": "kg:root",
            "target": job_id,
            "relation": "CREATED_JOB"
        })

    def handle_vehicle_assigned(self, event):
        job_id = self._job_id(event)
        vehicle_id = event.get("payload", {}).get("vehicle_id") or event.get("payload", {}).get("vehicleId")
        if not job_id or not vehicle_id:
            return
        self.graph["edges"].append({
            "source": job_id,
            "target": vehicle_id,
            "relation": "ASSIGNED_VEHICLE"
        })

    def handle_crew_assigned(self, event):
        job_id = self._job_id(event)
        crew_id = event.get("payload", {}).get("crew_id") or event.get("payload", {}).get("crewId")
        if not job_id or not crew_id:
            return
        self.graph["edges"].append({
            "source": job_id,
            "target": crew_id,
            "relation": "ASSIGNED_CREW"
        })

    def handle_delivery_completed(self, event):
        job_id = self._job_id(event)
        if not job_id:
            return
        self.graph["nodes"].append({
            "id": f"{job_id}:completed",
            "type": "EventState",
            "properties": {"status": "completed", "eventType": "DELIVERY_COMPLETED"}
        })
