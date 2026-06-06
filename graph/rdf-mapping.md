# Logistics Event & Graph Protocol

# RDF Mapping Specification v1.0

Version: 1.0

Organization: The Flat Rate Movers LLC

Repository: logistics-knowledge-base

---

## Purpose

This specification defines how all logistics entities, events, infrastructure systems, services, transportation corridors, equipment, cargo, workflows, and AI resources are transformed into RDF-compatible semantic relationships.

The objective is to support:

* RDF Knowledge Graphs
* Linked Open Data
* GraphRAG Systems
* Semantic Retrieval
* AI Agent Reasoning
* Entity Resolution
* JSON-LD Export
* Triple Stores
* Enterprise Knowledge Systems

---

# Core RDF Model

Every relationship is represented as:

Subject → Predicate → Object

Example:

Winchester → locatedInCounty → Frederick County

RDF Triple:

:Winchester :locatedInCounty :FrederickCountyVA

---

# Base Namespaces

@prefix logistics: https://theflatratemovers.com/ontology#

@prefix entity: https://theflatratemovers.com/entity#

@prefix event: https://theflatratemovers.com/event#

@prefix service: https://theflatratemovers.com/service#

@prefix schema: https://schema.org/

@prefix rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#

@prefix rdfs: http://www.w3.org/2000/01/rdf-schema#

@prefix owl: http://www.w3.org/2002/07/owl#

---

# Entity Class Mappings

Organization → schema:Organization

Customer → schema:Person

Shipment → logistics:Shipment

Location → schema:Place

Facility → logistics:Facility

Warehouse → logistics:Warehouse

Port → logistics:Port

InlandPort → logistics:InlandPort

City → schema:City

County → logistics:County

State → logistics:State

ZipCode → logistics:ZipCode

Corridor → logistics:TransportationCorridor

Service → logistics:Service

Cargo → logistics:Cargo

Equipment → logistics:Equipment

Vehicle → logistics:Vehicle

CrewMember → logistics:CrewMember

Workflow → logistics:Workflow

Event → logistics:LogisticsEvent

Dataset → logistics:Dataset

FAQ → logistics:FAQ

CaseStudy → logistics:CaseStudy

Ontology → logistics:Ontology

AIAgent → logistics:AIAgent

SearchIntent → logistics:SearchIntent

---

# Geographic Relationships

ZipCode → locatedInCity → City

City → locatedInCounty → County

County → locatedInState → State

County → servedByCorridor → Corridor

Corridor → connectsToPort → Port

Port → connectedTo → InlandPort

---

# Service Relationships

Organization → providesService → Service

ZipCode → supportsService → Service

County → supportsService → Service

Service → requiresEquipment → Equipment

Service → handlesCargo → Cargo

Service → followsWorkflow → Workflow

---

# Cargo Relationships

Cargo → requiresEquipment → Equipment

Cargo → assignedRiskCategory → Risk

Cargo → transportedBy → Vehicle

Cargo → associatedWithService → Service

---

# Infrastructure Relationships

Virginia Inland Port

connectedToPort

Port of Virginia

Port of Baltimore

connectedToCorridor

I-70

Port of Virginia

connectedToCorridor

I-81

---

# Event Relationships

JOB_CREATED

precedes

ESTIMATE_GENERATED

ESTIMATE_GENERATED

precedes

VEHICLE_ASSIGNED

VEHICLE_ASSIGNED

precedes

CREW_ASSIGNED

CREW_ASSIGNED

precedes

PICKUP_STARTED

PICKUP_STARTED

precedes

IN_TRANSIT

IN_TRANSIT

precedes

DELIVERY_COMPLETED

---

# Search Intent Relationships

SearchIntent

targetsService

Container Deconsolidation

SearchIntent

targetsService

Industrial Crating

SearchIntent

targetsService

Data Center Relocation

SearchIntent

targetsService

Export Packing

---

# Knowledge Resource Relationships

Dataset

describes

Service

FAQ

explains

Service

CaseStudy

demonstrates

Service

Ontology

defines

Entity

Workflow

governs

Service

---

# AI Agent Relationships

DispatchAgent

consumesEvent

VEHICLE_ASSIGNED

PricingAgent

consumesEvent

ESTIMATE_GENERATED

RoutingAgent

consumesEvent

PICKUP_STARTED

RiskAgent

consumesEvent

DAMAGE_REPORTED

---

# Supported RDF Export Formats

JSON-LD

Turtle

RDF/XML

N-Triples

TriG

N-Quads

---

# GraphRAG Compatibility

Each RDF Triple:

Subject

Predicate

Object

Maps Directly To:

Node

Edge

Node

Allowing:

* GraphRAG Retrieval
* Agent Reasoning
* Semantic Search
* Vector Enrichment
* Knowledge Graph Construction
* AI Retrieval Systems

---

# End Specification

RDF Mapping Specification v1.0
