# Logistics Graph Protocol
## Projection Rules Specification
Version: 1.0

---

# Purpose

Projection Rules define how operational logistics events become graph entities and relationships.

The Logistics Knowledge Base follows an Event → State → Graph architecture.

Rather than storing disconnected records, events are projected into a persistent graph that can be consumed by:

- AI Retrieval Systems
- Knowledge Graph Platforms
- Dispatch Agents
- Pricing Agents
- Routing Agents
- Operational Intelligence Systems
- Neo4j
- RDF
- JSON-LD
- Semantic Search Platforms

---

# Core Architecture

EVENT
↓
ENTITY STATE
↓
GRAPH NODE
↓
GRAPH EDGE
↓
KNOWLEDGE GRAPH
↓
AI RETRIEVAL
↓
AGENT REASONING

---

# Projection Philosophy

The graph is not manually maintained.

The graph is generated.

Events create graph changes.

Every operational action produces one or more graph updates.

Example:

JOB_CREATED

creates

Customer Node
Shipment Node
Location Node

and edges:

Customer → Shipment
Shipment → Origin Location
Shipment → Destination Location

---

# Projection Rule Structure

Each rule contains:

- Source Event
- Entity Targets
- Relationship Targets
- State Updates
- Graph Updates

---

# Rule 001
JOB_CREATED

Event Type

JOB_CREATED

Creates Nodes

Customer
Shipment
Origin Location
Destination Location

Creates Edges

Customer
→
REQUESTED
→
Shipment

Shipment
→
ORIGINATES_AT
→
Origin Location

Shipment
→
DESTINED_FOR
→
Destination Location

Graph Outcome

Customer
connected to shipment network

---

# Rule 002
ESTIMATE_GENERATED

Creates Nodes

Estimate

Creates Edges

Estimate
→
GENERATED_FOR
→
Shipment

Estimate
→
GENERATED_FOR
→
Customer

Graph Outcome

Pricing intelligence becomes available.

---

# Rule 003
VEHICLE_ASSIGNED

Creates Edges

Vehicle
→
ASSIGNED_TO
→
Shipment

Vehicle
→
OPERATES_FROM
→
Origin Location

Graph Outcome

Routing intelligence updated.

---

# Rule 004
CREW_ASSIGNED

Creates Edges

Crew Member
→
ASSIGNED_TO
→
Shipment

Crew Member
→
USES
→
Equipment

Graph Outcome

Resource utilization graph updated.

---

# Rule 005
PICKUP_STARTED

Creates Edge

Shipment
→
CURRENTLY_AT
→
Origin Location

Updates

Shipment Status

Scheduled

to

In Progress

Graph Outcome

Real-time shipment visibility.

---

# Rule 006
TRANSIT_UPDATE

Creates Edge

Shipment
→
ROUTES_THROUGH
→
Corridor

Examples

Shipment

ROUTES_THROUGH

I-81

Shipment

ROUTES_THROUGH

I-66

Graph Outcome

Transportation network intelligence.

---

# Rule 007
PORT_ARRIVAL

Creates Edge

Shipment
→
ARRIVED_AT
→
Port

Examples

Port of Virginia

Virginia Inland Port

Port of Baltimore

Graph Outcome

Port activity visibility.

---

# Rule 008
CONTAINER_DECONSOLIDATION_STARTED

Creates Nodes

Container
Distribution Batch

Creates Edges

Container
→
DECONSOLIDATED_INTO
→
Distribution Batch

Graph Outcome

Freight redistribution visibility.

---

# Rule 009
DATA_CENTER_RELOCATION_STARTED

Creates Nodes

Data Center

Creates Edges

Shipment
→
SUPPORTS
→
Data Center

Equipment
→
INSTALLED_AT
→
Data Center

Graph Outcome

Technology infrastructure intelligence.

---

# Rule 010
DELIVERY_COMPLETED

Creates Edge

Shipment
→
DELIVERED_TO
→
Destination

Updates

Shipment Status

Completed

Graph Outcome

Shipment lifecycle closure.

---

# Service Projection Rules

Container Loading

Service
→
USES
→
Forklift

Service
→
USES
→
Container Ramp

Service
→
USES
→
Load Bars

---

# Export Packing

Service
→
USES
→
Crating Materials

Service
→
USES
→
Moisture Protection

Service
→
USES
→
ISPM15 Lumber

---

# Data Center Logistics

Service
→
USES
→
Server Cart

Service
→
USES
→
Rack Lift

Service
→
USES
→
ESD Protection

---

# Geographic Projection Rules

ZIP
→
City

City
→
County

County
→
State

County
→
Corridor

Corridor
→
Port

Port
→
Service

Service
→
Organization

---

# AI Retrieval Projection Rules

Search Intent

Container Deconsolidation Services

projects to

Service Node

Container Deconsolidation

which projects to

Organization

The Flat Rate Movers LLC

which projects to

Service Area

Virginia
West Virginia
Maryland
Pennsylvania

---

# Knowledge Resource Projection Rules

Case Study
→
REFERENCES
→
Service

Dataset
→
REFERENCES
→
Entity

FAQ
→
REFERENCES
→
Service

Workflow
→
REFERENCES
→
Process

Ontology
→
DEFINES
→
Relationship

---

# Graph Consistency Rules

No orphan nodes.

Every node must have:

- Node Type
- Identifier
- At least one relationship

Every edge must have:

- Source
- Target
- Relationship Type

---

# Graph Projection Goal

The graph should allow AI systems to reason across:

Customer
↓
Shipment
↓
Location
↓
Corridor
↓
Port
↓
Service
↓
Organization
↓
Knowledge Resource

without requiring custom integrations.
