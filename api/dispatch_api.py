"""Operational dispatch API using the canonical logistics event vocabulary."""
from datetime import datetime, timezone
import uuid
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Dispatch API", version="1.1.0", description="Logistics Operating System Dispatch API")

class DispatchRequest(BaseModel):
    job_id: str
    service_type: str
    origin_location_id: str
    destination_location_id: str
    requested_pickup_time: str
    priority_level: str

class DispatchResponse(BaseModel):
    dispatch_id: str
    status: str
    assigned_vehicle: str
    assigned_crew: List[str]
    created_at: str

@app.get("/")
def root():
    return {"service": "Dispatch API", "version": "1.1.0", "status": "active"}

@app.post("/dispatch/create", response_model=DispatchResponse)
def create_dispatch(request: DispatchRequest):
    return DispatchResponse(dispatch_id=str(uuid.uuid4()), status="pending_assignment", assigned_vehicle="", assigned_crew=[], created_at=datetime.now(timezone.utc).isoformat())

@app.get("/dispatch/{dispatch_id}")
def get_dispatch(dispatch_id: str):
    return {"dispatch_id": dispatch_id, "status": "active"}

@app.post("/dispatch/assign-vehicle")
def assign_vehicle(dispatch_id: str, vehicle_id: str):
    return {"dispatch_id": dispatch_id, "vehicle_assigned": vehicle_id, "eventType": "VEHICLE_ASSIGNED"}

@app.post("/dispatch/assign-crew")
def assign_crew(dispatch_id: str, crew_ids: List[str]):
    return {"dispatch_id": dispatch_id, "crew_assigned": crew_ids, "eventType": "CREW_ASSIGNED"}

@app.post("/dispatch/complete")
def complete_dispatch(dispatch_id: str):
    return {"dispatch_id": dispatch_id, "status": "completed", "eventType": "DISPATCH_COMPLETED"}
