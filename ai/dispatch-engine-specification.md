# Dispatch Engine Specification

## Logistics Event & Graph Protocol v1.0

Repository Path:

/ai/dispatch-engine-specification.md

---

# PURPOSE

The Dispatch Engine is the operational decision engine responsible for converting logistics events, graph intelligence, current state, routing recommendations, risk analysis, and customer requirements into executable dispatch decisions.

The Dispatch Engine acts as the central operational coordinator of the Logistics Operating System.

---

# SYSTEM ROLE

The Dispatch Engine sits between:

Customer Intent
↓
Agent Layer
↓
Dispatch Engine
↓
Operational Execution

---

# PRIMARY OBJECTIVES

1. Assign jobs to crews
2. Assign jobs to vehicles
3. Validate equipment requirements
4. Balance workloads
5. Reduce operational risk
6. Maximize resource utilization
7. Minimize travel time
8. Ensure service compatibility
9. Maintain service-level objectives
10. Generate dispatch events

---

# INPUT SOURCES

## Event Stream

Consumes:

* JOB_CREATED
* ESTIMATE_GENERATED
* VEHICLE_ASSIGNED
* CREW_ASSIGNED
* PICKUP_STARTED
* DELIVERY_COMPLETED
* DELAY_REPORTED
* DAMAGE_REPORTED
* ROUTE_UPDATED

---

## State Layer

Consumes:

* Current Jobs
* Current Vehicles
* Current Crews
* Current Equipment
* Current Shipments

Source:

/state/current_state_store.py

---

## Graph Layer

Consumes:

* Service relationships
* Historical performance
* Geographic intelligence
* Equipment relationships
* Resource availability

Source:

Neo4j Graph

---

## Agent Inputs

Receives recommendations from:

* Routing Agent
* Pricing Agent
* Risk Agent
* Technology Logistics Agent
* Graph Retrieval Agent

---

# DISPATCH DECISION MODEL

Dispatch Score Formula

DispatchScore =

ServiceCompatibility +
ResourceAvailability +
DistanceScore +
HistoricalPerformance +
RiskAdjustment +
EquipmentMatch

---

# CREW MATCHING FACTORS

Factors:

* Certifications
* TWIC Status
* Equipment Experience
* Service History
* Availability
* Shift Status
* Distance From Job

---

# VEHICLE MATCHING FACTORS

Factors:

* Capacity
* Payload
* Liftgate Availability
* Equipment Compatibility
* Fuel Efficiency
* Current Route
* Vehicle Status

---

# SERVICE SPECIALIZATION

Supported Services:

* Residential Moving
* Commercial Moving
* Industrial Moving
* Export Packing
* Industrial Crating
* Container Loading
* Container Unloading
* Container Deconsolidation
* Cross Docking
* Transloading
* Warehouse Labor
* TWIC Labor
* Port Logistics
* Data Center Relocation
* Server Relocation
* Technology Asset Transportation

---

# DISPATCH WORKFLOW

JOB_CREATED
↓
Resource Search
↓
Crew Ranking
↓
Vehicle Ranking
↓
Risk Review
↓
Routing Review
↓
Dispatch Decision
↓
CREW_ASSIGNED
↓
VEHICLE_ASSIGNED

---

# OUTPUT EVENTS

May Generate:

* CREW_ASSIGNED
* VEHICLE_ASSIGNED
* EQUIPMENT_ASSIGNED
* DISPATCH_COMPLETED
* DISPATCH_FAILED
* RESOURCE_SHORTAGE
* RISK_ESCALATION

---

# MACHINE CONTRACT

{
"engine":"DispatchEngine",
"version":"1.0",
"eventDriven":true,
"graphAware":true,
"stateAware":true,
"supportsOptimization":true,
"supportsAutomation":true
}
