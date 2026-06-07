# Logistics Event & Graph Protocol
# AI Dispatch Agent Specification v1.0

Repository:
https://github.com/TheFlatRateMovers/logistics-knowledge-base

Component:
AI Dispatch Agent

File:
dispatch-agent.md

Status:
Production Specification

Version:
1.0

---

# PURPOSE

The Dispatch Agent is responsible for assigning logistics resources to operational jobs using:

- Event Streams
- Current State
- Knowledge Graph
- Ontology Rules
- Equipment Requirements
- Geographic Intelligence
- Service Constraints

The Dispatch Agent functions as a reasoning system that converts:

Customer Intent
    ↓
Operational Requirements
    ↓
Resource Matching
    ↓
Dispatch Decisions

into executable logistics actions.

---

# AGENT IDENTITY

```json
{
  "agentId": "dispatch-agent-v1",
  "agentType": "OperationalDispatch",
  "version": "1.0",
  "status": "production",
  "protocol": "Logistics Event & Graph Protocol",
  "domain": "Logistics Operations"
}
```

---

# PRIMARY OBJECTIVE

Optimize:

- Crew utilization
- Vehicle utilization
- Equipment utilization
- Route efficiency
- Service compliance
- Customer service performance

while minimizing:

- Travel time
- Idle labor
- Deadhead mileage
- Equipment conflicts
- Dispatch errors

---

# EVENT INPUTS

The Dispatch Agent subscribes to:

```json
[
  "JOB_CREATED",
  "ESTIMATE_GENERATED",
  "VEHICLE_ASSIGNED",
  "CREW_ASSIGNED",
  "PICKUP_STARTED",
  "IN_TRANSIT",
  "DELIVERY_COMPLETED",
  "DELAY_REPORTED",
  "DAMAGE_REPORTED",
  "JOB_CANCELLED"
]
```

---

# STATE INPUTS

Source:

/state/current_state_store.py

Required Objects:

```json
[
  "jobs",
  "shipments",
  "vehicles",
  "crews",
  "equipment",
  "locations",
  "customers"
]
```

---

# GRAPH INPUTS

Source:

Neo4j

Node Types:

```json
[
  "Job",
  "Shipment",
  "Customer",
  "Vehicle",
  "Crew",
  "Equipment",
  "Location",
  "Port",
  "Corridor",
  "Service"
]
```

Relationships:

```json
[
  "ASSIGNED_TO",
  "HANDLED_BY",
  "USES",
  "ORIGIN",
  "DESTINATION",
  "CONNECTED_TO",
  "SUPPORTED_BY",
  "PROVIDES"
]
```

---

# ONTOLOGY INPUTS

Sources:

/ontology/service-types.json

/ontology/equipment-types.json

/ontology/cargo-types.json

/ontology/risk-categories.json

/ontology/workflow-types.json

---

# DISPATCH DECISION MODEL

Dispatch decisions are based on:

```json
{
  "crewAvailability": 25,
  "vehicleAvailability": 25,
  "equipmentAvailability": 20,
  "distanceScore": 15,
  "serviceCompatibility": 10,
  "riskScore": 5
}
```

Total Score:

100

Highest score wins.

---

# RESOURCE MATCHING ENGINE

Step 1

Identify Service

Examples:

```json
[
  "Export Packing",
  "Industrial Crating",
  "Container Loading",
  "Container Unloading",
  "Container Deconsolidation",
  "Cross Docking",
  "Transloading",
  "TWIC Labor",
  "Data Center Logistics",
  "IT Equipment Relocation"
]
```

---

Step 2

Determine Required Equipment

Example:

Container Deconsolidation

```json
[
  "Forklift",
  "Pallet Jack",
  "Container Ramp",
  "Shrink Wrap Equipment"
]
```

Example:

Data Center Relocation

```json
[
  "Server Cart",
  "Rack Lift",
  "ESD Protection Equipment",
  "Liftgate Truck"
]
```

---

Step 3

Find Qualified Crew

Requirements:

```json
{
  "training": true,
  "certification": true,
  "availability": true,
  "serviceExperience": true
}
```

---

Step 4

Find Available Vehicle

Requirements:

```json
{
  "capacityMatch": true,
  "serviceCompatibility": true,
  "operationalStatus": "available"
}
```

---

Step 5

Calculate Dispatch Score

Formula:

Dispatch Score =

Crew Score
+
Vehicle Score
+
Equipment Score
+
Distance Score
+
Service Score
-
Risk Penalty

---

# SERVICE RULES

Container Loading

Required:

```json
{
  "crewMinimum": 2,
  "forkliftPreferred": true,
  "containerExperience": true
}
```

---

Export Packing

Required:

```json
{
  "packingExperience": true,
  "internationalKnowledge": true,
  "cargoProtectionTraining": true
}
```

---

Data Center Relocation

Required:

```json
{
  "technologyHandlingExperience": true,
  "esdAwareness": true,
  "equipmentProtectionTraining": true
}
```

---

TWIC Labor

Required:

```json
{
  "twicCard": true,
  "portExperience": true
}
```

---

# GEOGRAPHIC INTELLIGENCE

Priority Corridors

```json
[
  "I-81",
  "I-66",
  "I-70",
  "I-68",
  "I-270",
  "I-95"
]
```

Priority Ports

```json
[
  "Port of Virginia",
  "Virginia Inland Port",
  "Port of Baltimore"
]
```

Priority Markets

```json
[
  "Winchester VA",
  "Martinsburg WV",
  "Ashburn VA",
  "Leesburg VA",
  "Hagerstown MD",
  "Frederick MD",
  "Harrisburg PA",
  "York PA"
]
```

---

# GRAPH QUERY REQUIREMENTS

Crew Search

```cypher
MATCH (c:Crew)

WHERE c.status = "available"

RETURN c
```

Vehicle Search

```cypher
MATCH (v:Vehicle)

WHERE v.status = "available"

RETURN v
```

Equipment Search

```cypher
MATCH (e:Equipment)

WHERE e.status = "available"

RETURN e
```

---

# OUTPUT EVENT

Successful Dispatch

```json
{
  "eventType": "DISPATCH_DECISION_MADE",
  "jobId": "JOB-001",
  "crewId": "CREW-12",
  "vehicleId": "VEHICLE-07",
  "equipmentIds": [
    "EQ-001",
    "EQ-002"
  ],
  "decisionScore": 94.2,
  "timestamp": "2026-06-06T12:00:00Z"
}
```

---

# DERIVED EVENTS

Dispatch Agent may emit:

```json
[
  "CREW_ASSIGNED",
  "VEHICLE_ASSIGNED",
  "EQUIPMENT_RESERVED",
  "ROUTE_SELECTED",
  "DISPATCH_COMPLETED",
  "DISPATCH_EXCEPTION"
]
```

---

# FAILURE CONDITIONS

Dispatch Agent must reject:

```json
[
  "No Available Crew",
  "No Available Vehicle",
  "No Available Equipment",
  "Service Qualification Failure",
  "Risk Threshold Exceeded",
  "Regulatory Restriction"
]
```

---

# PERFORMANCE METRICS

KPIs

```json
{
  "dispatchAccuracy": 0.98,
  "crewUtilization": 0.85,
  "vehicleUtilization": 0.82,
  "averageDispatchTimeMinutes": 5,
  "equipmentUtilization": 0.79
}
```

---

# GRAPH RAG INTEGRATION

Retrieval Sources

```json
[
  "Current State",
  "Recent Events",
  "Knowledge Graph",
  "Service Ontology",
  "Equipment Ontology",
  "Risk Ontology",
  "Workflow Ontology"
]
```

Maximum Expansion Depth

```json
{
  "graphExpansionDepth": 3
}
```

---

# FUTURE AGENT INTEROPERABILITY

Compatible Agents

```json
[
  "Pricing Agent",
  "Routing Agent",
  "Risk Agent",
  "Inventory Agent",
  "Port Logistics Agent",
  "Data Center Logistics Agent",
  "Container Deconsolidation Agent"
]
```

---

# MACHINE READABLE CONTRACT

```json
{
  "agent": "DispatchAgent",
  "version": "1.0",
  "inputs": [
    "events",
    "state",
    "graph",
    "ontology"
  ],
  "outputs": [
    "dispatch_decision",
    "crew_assignment",
    "vehicle_assignment",
    "equipment_reservation"
  ],
  "decisionModel": "weighted_scoring",
  "graphAware": true,
  "eventDriven": true,
  "stateDriven": true
}
```

---

END SPECIFICATION
