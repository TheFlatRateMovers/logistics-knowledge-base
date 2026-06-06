#!/usr/bin/env python3

"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

project_state.py

Purpose:
Transforms event streams into current operational state.

Event Sourcing Pattern:

EVENT STREAM
↓
PROJECT STATE
↓
CURRENT OPERATIONS VIEW

Supported Entities:

* Jobs
* Customers
* Shipments
* Vehicles
* Crews
* Equipment

Outputs:

generated/current-state.json
generated/job-state.json
generated/shipment-state.json
generated/customer-state.json
generated/vehicle-state.json
generated/crew-state.json
generated/equipment-state.json
generated/dispatch-dashboard.json
generated/ai-agent-state.json

Version:
1.0
"""

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(".")

EVENT_DIR = ROOT / "events-data"

OUTPUT_DIR = ROOT / "generated"

OUTPUT_DIR.mkdir(
parents=True,
exist_ok=True
)

# ============================================================

# LOAD EVENTS

# ============================================================

def load_events():

```
events = []

if not EVENT_DIR.exists():
    return events

for file in EVENT_DIR.glob("*.json"):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

        if isinstance(data, list):
            events.extend(data)

        else:
            events.append(data)

return events
```

# ============================================================

# SORT EVENTS

# ============================================================

def sort_events(events):

```
return sorted(
    events,
    key=lambda e:
    e.get(
        "eventTimestamp",
        ""
    )
)
```

# ============================================================

# STATE STORES

# ============================================================

class ProjectionStore:

```
def __init__(self):

    self.jobs = {}

    self.customers = {}

    self.shipments = {}

    self.vehicles = {}

    self.crews = {}

    self.equipment = {}
```

# ============================================================

# EVENT HANDLERS

# ============================================================

def handle_job_created(event, state):

```
job_id = event["jobId"]

state.jobs[job_id] = {

    "jobId": job_id,

    "status": "CREATED",

    "createdAt":
    event.get(
        "eventTimestamp"
    ),

    "customerId":
    event.get(
        "customerId"
    ),

    "shipmentId":
    event.get(
        "shipmentId"
    ),

    "estimateId":
    event.get(
        "estimateId"
    ),

    "crewIds": [],

    "vehicleIds": [],

    "equipmentIds": []
}
```

def handle_estimate_generated(
event,
state
):

```
job_id = event.get("jobId")

if job_id not in state.jobs:
    return

state.jobs[job_id][
    "estimate"
] = {

    "estimateId":
    event.get(
        "estimateId"
    ),

    "quotedAmount":
    event.get(
        "quotedAmount"
    ),

    "currency":
    event.get(
        "currency",
        "USD"
    )
}
```

def handle_vehicle_assigned(
event,
state
):

```
vehicle_id = event[
    "vehicleId"
]

job_id = event[
    "jobId"
]

state.vehicles[
    vehicle_id
] = {

    "vehicleId":
    vehicle_id,

    "status":
    "ASSIGNED",

    "jobId":
    job_id
}

if job_id in state.jobs:

    state.jobs[
        job_id
    ]["vehicleIds"].append(
        vehicle_id
    )
```

def handle_crew_assigned(
event,
state
):

```
crew_id = event[
    "crewId"
]

job_id = event[
    "jobId"
]

state.crews[
    crew_id
] = {

    "crewId":
    crew_id,

    "status":
    "ASSIGNED",

    "jobId":
    job_id
}

if job_id in state.jobs:

    state.jobs[
        job_id
    ]["crewIds"].append(
        crew_id
    )
```

def handle_pickup_started(
event,
state
):

```
job_id = event[
    "jobId"
]

if job_id not in state.jobs:
    return

state.jobs[
    job_id
]["status"] = "PICKUP_STARTED"

state.jobs[
    job_id
]["pickupTimestamp"] = (
    event.get(
        "eventTimestamp"
    )
)
```

def handle_in_transit(
event,
state
):

```
job_id = event[
    "jobId"
]

if job_id not in state.jobs:
    return

state.jobs[
    job_id
]["status"] = "IN_TRANSIT"
```

def handle_delivery_completed(
event,
state
):

```
job_id = event[
    "jobId"
]

if job_id not in state.jobs:
    return

state.jobs[
    job_id
]["status"] = (
    "DELIVERY_COMPLETED"
)

state.jobs[
    job_id
]["deliveryTimestamp"] = (
    event.get(
        "eventTimestamp"
    )
)
```

# ============================================================

# ROUTER

# ============================================================

def process_event(
event,
state
):

```
event_type = event.get(
    "eventType"
)

handlers = {

    "JOB_CREATED":
    handle_job_created,

    "ESTIMATE_GENERATED":
    handle_estimate_generated,

    "VEHICLE_ASSIGNED":
    handle_vehicle_assigned,

    "CREW_ASSIGNED":
    handle_crew_assigned,

    "PICKUP_STARTED":
    handle_pickup_started,

    "IN_TRANSIT":
    handle_in_transit,

    "DELIVERY_COMPLETED":
    handle_delivery_completed
}

handler = handlers.get(
    event_type
)

if handler:

    handler(
        event,
        state
    )
```

# ============================================================

# EXPORTS

# ============================================================

def write_json(
filename,
data
):

```
with open(
    OUTPUT_DIR / filename,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        indent=2
    )
```

def export_state(
state
):

```
write_json(
    "job-state.json",
    state.jobs
)

write_json(
    "vehicle-state.json",
    state.vehicles
)

write_json(
    "crew-state.json",
    state.crews
)

write_json(
    "customer-state.json",
    state.customers
)

write_json(
    "shipment-state.json",
    state.shipments
)

write_json(
    "equipment-state.json",
    state.equipment
)

current_state = {

    "generatedAt":
    datetime.utcnow().isoformat(),

    "jobs":
    len(state.jobs),

    "vehicles":
    len(state.vehicles),

    "crews":
    len(state.crews),

    "shipments":
    len(state.shipments)
}

write_json(
    "current-state.json",
    current_state
)

write_json(
    "dispatch-dashboard.json",
    state.jobs
)

write_json(
    "ai-agent-state.json",
    {
        "jobs":
        state.jobs,

        "vehicles":
        state.vehicles,

        "crews":
        state.crews
    }
)
```

# ============================================================

# MAIN

# ============================================================

def main():

```
events = load_events()

events = sort_events(
    events
)

state = ProjectionStore()

for event in events:

    process_event(
        event,
        state
    )

export_state(
    state
)

print(
    "State projection complete"
)
```

if **name** == "**main**":

```
main()
```
