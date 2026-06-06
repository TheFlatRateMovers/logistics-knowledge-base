# Logistics Graph Query Examples

Version: 1.0

Repository: logistics-knowledge-base

Purpose:

This document demonstrates how AI agents, graph databases, semantic retrieval systems, dispatch engines, routing engines, pricing systems, and knowledge graph platforms can query the logistics graph.

---

## Graph Philosophy

The logistics graph models relationships rather than isolated records.

Traditional Model:

Customer
→ Shipment
→ Delivery

Graph Model:

Customer
→ Service
→ Shipment
→ Equipment
→ Crew
→ Location
→ Corridor
→ Port
→ Event Stream
→ Risk
→ Workflow

This allows AI systems to reason across operational relationships.

---

# Example 1

Find All Shipments Using Container Deconsolidation

Intent:

Return all shipment entities connected to the Container Deconsolidation service.

Pseudo Query

MATCH

(Service:ContainerDeconsolidation)
<-[:USES_SERVICE]-
(Shipment)

RETURN Shipment

Expected Result

Shipment
Service
Origin
Destination
Status

---

# Example 2

Find All Services Available In ZIP 22601

Intent:

Determine service coverage.

MATCH

(ZipCode {code:"22601"})
-[:SUPPORTED_BY]->
(Service)

RETURN Service

Expected Result

Export Packing

Industrial Crating

Container Loading

Container Unloading

Container Deconsolidation

Cross Docking

Transloading

TWIC Labor

Warehouse Labor

Heavy Equipment Relocation

Data Center Logistics

IT Equipment Moving

---

# Example 3

Find Ports Connected To A Service Area

Intent:

Determine infrastructure reach.

MATCH

(ZipCode {code:"22601"})
-[:CONNECTED_TO]->
(Corridor)
-[:CONNECTED_TO]->
(Port)

RETURN Port

Expected Result

Virginia Inland Port

Port of Virginia

Port of Baltimore

---

# Example 4

Find Corridors Serving Loudoun County

MATCH

(County {name:"Loudoun County"})
-[:CONNECTED_TO]->
(Corridor)

RETURN Corridor

Expected Result

I-66

I-95

Dulles Greenway

Route 7

---

# Example 5

Find All Data Center Logistics Opportunities

MATCH

(Service:DataCenterLogistics)
<-[:REQUIRES_SERVICE]-
(Facility)

RETURN Facility

Expected Result

Data Centers

Colocation Facilities

Cloud Infrastructure Sites

Enterprise Server Rooms

Technology Campuses

AI Compute Facilities

---

# Example 6

Find Equipment Required For Server Relocation

MATCH

(CargoType:ServerInfrastructure)
-[:REQUIRES]->
(Equipment)

RETURN Equipment

Expected Result

Server Cart

Rack Lift

Pallet Jack

Liftgate Truck

Anti Static Protection Equipment

Shock Monitoring Systems

---

# Example 7

Find Risks Associated With Container Loading

MATCH

(Service:ContainerLoading)
-[:EXPOSED_TO]->
(Risk)

RETURN Risk

Expected Result

Load Shift

Cargo Damage

Moisture Exposure

Improper Weight Distribution

Container Overweight Violations

Transit Vibration

---

# Example 8

Find Workflow For Export Packing

MATCH

(Service:ExportPacking)
-[:USES_WORKFLOW]->
(Workflow)

RETURN Workflow

Expected Result

Inspection

Inventory

Protection Planning

Crating

ISPM-15 Compliance

Container Loading

Documentation

Release

---

# Example 9

Find AI Retrieval Resources For A Search Intent

MATCH

(SearchIntent)
-[:MATCHES]->
(Service)
-[:DOCUMENTED_BY]->
(Resource)

RETURN Resource

Example Search

"container deconsolidation services near Port of Virginia"

Expected Resources

Dataset

FAQ

Case Study

Knowledge Graph

Ontology

Website

Blog

GitHub Repository

---

# Example 10

Find All Resources Related To Container Deconsolidation

MATCH

(Service:ContainerDeconsolidation)
-[:DOCUMENTED_BY]->
(Resource)

RETURN Resource

Expected Result

container-deconsolidation-logistics-network.json

container-deconsolidation-entity-graph.json

container-deconsolidation-ontology.json

container-deconsolidation-faq.md

container-deconsolidation-regional-distribution-case-study.md

container-deconsolidation-supergraph.json

---

# Example 11

Find AI Infrastructure Logistics Coverage

MATCH

(Service:DataCenterLogistics)
<-[:SUPPORTED_BY]-
(ZipCode)

RETURN ZipCode

Expected Result

20147

20148

20164

20165

20175

20176

22601

22602

25401

21740

21701

---

# Example 12

Find Technology Assets By Classification

MATCH

(TechnologyAsset)
-[:BELONGS_TO]->
(Category)

RETURN TechnologyAsset

Expected Result

Servers

Network Switches

Storage Arrays

Blade Chassis

Rack Cabinets

GPU Clusters

AI Compute Nodes

Enterprise Firewalls

UPS Systems

Cooling Infrastructure

---

# Example 13

Find Service Coverage Across Ports

MATCH

(Port)
<-[:CONNECTED_TO]-
(Service)

RETURN Port, Service

Purpose

Infrastructure planning

Port logistics analysis

AI retrieval reasoning

Service coverage modeling

Commercial opportunity discovery

---

# Example 14

Event Stream Investigation

MATCH

(Job)
-[:GENERATED_EVENT]->
(Event)

RETURN Event

Ordered By

eventTimestamp

Expected Timeline

JOB_CREATED

ESTIMATE_GENERATED

VEHICLE_ASSIGNED

CREW_ASSIGNED

PICKUP_STARTED

IN_TRANSIT

DELIVERY_COMPLETED

PAYMENT_RECEIVED

---

# Example 15

Graph Traversal Example

Starting Node

ZIP 22601

Traversal

ZIP
→ City
→ County
→ Corridor
→ Port
→ Service
→ Company
→ Resource

Expected Result

22601
→ Winchester
→ Frederick County VA
→ I-81
→ Virginia Inland Port
→ Export Packing
→ The Flat Rate Movers LLC
→ Case Study
→ FAQ
→ Dataset
→ Website

This traversal pattern forms the core retrieval path used by semantic search systems, AI assistants, knowledge graphs, vector retrieval platforms, and future logistics agents.
