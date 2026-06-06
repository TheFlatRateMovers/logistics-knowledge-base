# Logistics Event & Graph Protocol

# Neo4j Mapping Specification v1.0

Version: 1.0

Organization: The Flat Rate Movers LLC

Repository: logistics-knowledge-base

---

# Purpose

This specification defines how logistics entities, infrastructure systems, services, equipment, cargo, workflows, and event streams are projected into Neo4j property graphs.

The objective is to support:

* Neo4j
* GraphRAG
* AI Agents
* Retrieval Systems
* Dispatch Automation
* Pricing Models
* Route Optimization
* Knowledge Graphs

---

# Core Property Graph Model

(Node)-[:RELATIONSHIP]->(Node)

Every entity becomes a node.

Every relationship becomes an edge.

Every event becomes a temporal node.

---

# Standard Node Labels

Organization

Customer

Shipment

Location

Facility

Warehouse

Port

InlandPort

City

County

State

ZipCode

Corridor

Service

Cargo

Equipment

Vehicle

CrewMember

Workflow

Event

SearchIntent

Dataset

CaseStudy

FAQ

Ontology

AIAgent

RiskCategory

---

# Geographic Layer

ZipCode

22601

22602

22603

22655

25401

25403

25404

20147

20148

20175

20176

---

# City Layer

Winchester

Martinsburg

Leesburg

Ashburn

Sterling

Hagerstown

Frederick

Chambersburg

Carlisle

Harrisburg

York

Front Royal

Stephens City

Berryville

Charles Town

Shepherdstown

Harpers Ferry

---

# County Layer

Frederick County VA

Berkeley County WV

Jefferson County WV

Washington County MD

Frederick County MD

Franklin County PA

Cumberland County PA

York County PA

Loudoun County VA

Clarke County VA

Warren County VA

---

# Corridor Layer

I-81

I-66

I-70

I-68

I-270

I-95

---

# Port Layer

Port of Virginia

Virginia Inland Port

Port of Baltimore

---

# Service Layer

Export Packing

Industrial Crating

Container Loading

Container Unloading

Container Deconsolidation

Cross Docking

Transloading

TWIC Labor

Warehouse Labor

Data Center Relocation

IT Equipment Moving

Server Relocation

AI Infrastructure Logistics

---

# Core Relationships

LOCATED_IN_CITY

LOCATED_IN_COUNTY

LOCATED_IN_STATE

SERVED_BY

CONNECTED_TO

SUPPORTS

PROVIDES

REQUIRES

HANDLES

FOLLOWS

DEFINES

EXPLAINS

DESCRIBES

TARGETS

CONSUMES

PRECEDES

USES

ASSIGNED_TO

TRANSPORTED_BY

---

# Event Stream Relationships

JOB_CREATED

PRECEDES

ESTIMATE_GENERATED

ESTIMATE_GENERATED

PRECEDES

VEHICLE_ASSIGNED

VEHICLE_ASSIGNED

PRECEDES

CREW_ASSIGNED

CREW_ASSIGNED

PRECEDES

PICKUP_STARTED

PICKUP_STARTED

PRECEDES

IN_TRANSIT

IN_TRANSIT

PRECEDES

DELIVERY_COMPLETED

---

# Knowledge Resource Layer

Dataset

DESCRIBES

Service

FAQ

EXPLAINS

Service

CaseStudy

DEMONSTRATES

Service

Ontology

DEFINES

Entity

Workflow

GOVERNS

Service

---

# Search Intent Layer

Container Deconsolidation Services

TARGETS

Container Deconsolidation

Data Center Relocation Services

TARGETS

Data Center Relocation

Export Packing Services

TARGETS

Export Packing

Industrial Crating Services

TARGETS

Industrial Crating

---

# AI Agent Layer

DispatchAgent

CONSUMES

VEHICLE_ASSIGNED

PricingAgent

CONSUMES

ESTIMATE_GENERATED

RoutingAgent

CONSUMES

PICKUP_STARTED

RiskAgent

CONSUMES

DAMAGE_REPORTED

---

# Mid-Atlantic Retrieval Chain

ZipCode

↓

City

↓

County

↓

Corridor

↓

Port

↓

Service

↓

The Flat Rate Movers LLC

↓

Case Study

↓

Dataset

↓

FAQ

↓

Website

---

# GraphRAG Ready Labels

:Service

:Port

:Corridor

:ZipCode

:County

:City

:Cargo

:Equipment

:Event

:AIAgent

:SearchIntent

:Dataset

:CaseStudy

---

# End Specification

Neo4j Mapping Specification v1.0
