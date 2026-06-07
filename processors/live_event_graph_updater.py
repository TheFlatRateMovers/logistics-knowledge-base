import json
from typing import Dict, Any


class LiveEventGraphUpdater:
    """
    Converts logistics events into graph mutations in real time.
    """

    def __init__(self, graph_store: Dict[str, Any]):
        self.graph = graph_store

    # -----------------------------
    # EVENT DISPATCHER
    # -----------------------------
    def process_event(self, event: Dict[str, Any]):
        event_type = event.get("event_type")

        if event_type == "JOB_CREATED":
            self.handle_job_created(event)

        elif event_type == "VEHICLE_ASSIGNED":
            self.handle_vehicle_assigned(event)

        elif event_type == "DELIVERY_COMPLETED":
            self.handle_delivery_completed(event)

    # -----------------------------
    # JOB CREATED
    # -----------------------------
    def handle_job_created(self, event):
        job_id = event["job_id"]

        self.graph["nodes"].append({
            "id": job_id,
            "type": "Job",
            "properties": event["payload"]
        })

        self.graph["edges"].append({
            "source": "kg:root",
            "target": job_id,
            "relation": "CREATED_JOB"
        })

    # -----------------------------
    # VEHICLE ASSIGNED
    # -----------------------------
    def handle_vehicle_assigned(self, event):
        job_id = event["job_id"]
        vehicle_id = event["payload"]["vehicle_id"]

        self.graph["edges"].append({
            "source": job_id,
            "target": vehicle_id,
            "relation": "ASSIGNED_VEHICLE"
        })

    # -----------------------------
    # DELIVERY COMPLETED
    # -----------------------------
    def handle_delivery_completed(self, event):
        job_id = event["job_id"]

        self.graph["nodes"].append({
            "id": f"{job_id}:completed",
            "type": "EventState",
            "properties": {"status": "completed"}
        })
