# Logistics Event & Graph Protocol
# GraphRAG Retrieval Specification v1.0

Repository:
https://github.com/TheFlatRateMovers/logistics-knowledge-base

Author:
The Flat Rate Movers LLC

Status:
Production Specification

Version:
1.0

------------------------------------------------------------
PURPOSE
------------------------------------------------------------

This specification defines how GraphRAG systems retrieve,
assemble, rank, expand, and reason over logistics data.

The objective is to provide a canonical retrieval architecture
for:

- AI Agents
- LLM Retrieval
- GraphRAG Pipelines
- Neo4j Knowledge Graphs
- RDF Triple Stores
- Vector Search Engines
- Dispatch Systems
- Pricing Systems
- Routing Systems
- Logistics Intelligence Platforms

This specification establishes:

Event → State → Graph → Context → Reasoning

as the official retrieval architecture.

------------------------------------------------------------
CORE PRINCIPLE
------------------------------------------------------------

Traditional RAG:

Documents
↓
Chunks
↓
Embeddings
↓
Answer

GraphRAG:

Events
↓
State
↓
Knowledge Graph
↓
Graph Expansion
↓
Reasoning Context
↓
Answer

GraphRAG always operates on relationships.

------------------------------------------------------------
CANONICAL DATA FLOW
------------------------------------------------------------

Source Systems

Events
Entities
Ontologies
Datasets
Case Studies
FAQs
Workflows

↓

Event Store

↓

State Projection Engine

↓

Knowledge Graph

↓

Vector Store

↓

GraphRAG Retrieval Engine

↓

AI Agent

↓

Response

------------------------------------------------------------
RETRIEVAL LAYERS
------------------------------------------------------------

Layer 1

Ontology Layer

Purpose:

Defines vocabulary.

Sources:

/ontology/entity-types.json
/ontology/service-types.json
/ontology/cargo-types.json
/ontology/equipment-types.json
/ontology/relationship-types.json
/ontology/risk-categories.json
/ontology/event-types.json
/ontology/workflow-types.json

Retrieval Weight:

High

------------------------------------------------------------

Layer 2

Entity Layer

Purpose:

Defines operational objects.

Sources:

/entities/customer.schema.json
/entities/shipment.schema.json
/entities/location.schema.json
/entities/equipment.schema.json

Retrieval Weight:

Very High

------------------------------------------------------------

Layer 3

Event Layer

Purpose:

Defines operational history.

Sources:

/events/*.json

Examples:

JOB_CREATED
ESTIMATE_GENERATED
VEHICLE_ASSIGNED
CREW_ASSIGNED
PICKUP_STARTED
DELIVERY_COMPLETED

Retrieval Weight:

Highest

Reason:

Events provide causality.

------------------------------------------------------------

Layer 4

State Layer

Purpose:

Defines current reality.

Source:

/state/current_state_store.py

Example:

Shipment:

Current Status
Assigned Vehicle
Assigned Crew
Current Location

Retrieval Weight:

Highest

------------------------------------------------------------

Layer 5

Graph Layer

Purpose:

Relationship discovery.

Sources:

Neo4j
GraphRAG
Knowledge Graph

Retrieval Weight:

Highest

------------------------------------------------------------
GRAPH RETRIEVAL MODEL
------------------------------------------------------------

Node Categories

Organization

Customer

Shipment

Job

Vehicle

Crew

Equipment

Location

Port

County

City

ZipCode

Service

SearchIntent

LogisticsEvent

------------------------------------------------------------

Relationship Categories

REQUESTED_BY

ASSIGNED_TO

HANDLED_BY

USES

ORIGIN

DESTINATION

LOCATED_IN

PROVIDES

CONNECTED_TO

SUPPORTED_BY

AFFECTS

GENERATED_BY

TARGETS_LOCATION

MATCHES_SERVICE

------------------------------------------------------------
GRAPH EXPANSION RULES
------------------------------------------------------------

Expansion Depth 1

Direct Neighbors

Example:

Shipment
→ Vehicle
→ Crew

------------------------------------------------------------

Expansion Depth 2

Operational Context

Shipment
→ Vehicle
→ Equipment

Shipment
→ Origin
→ County

Shipment
→ Destination
→ Corridor

------------------------------------------------------------

Expansion Depth 3

Business Context

Shipment
→ Service
→ Port
→ Search Intent

------------------------------------------------------------

Maximum Recommended Depth

4

Reason:

Prevents graph explosion.

------------------------------------------------------------
CONTEXT ASSEMBLY MODEL
------------------------------------------------------------

Step 1

Identify Target Entity

Example:

"Container Deconsolidation"

↓

Step 2

Retrieve Direct Relationships

Service
→ Locations
→ Ports
→ Corridors

↓

Step 3

Retrieve Event Context

Recent Jobs
Recent Shipments

↓

Step 4

Retrieve Ontology Context

Service Definitions

↓

Step 5

Assemble Final Context

------------------------------------------------------------
RETRIEVAL PRIORITY SCORES
------------------------------------------------------------

Current State

100

Recent Events

95

Direct Relationships

90

Service Definitions

85

Case Studies

80

FAQs

75

Datasets

70

Historical Events

65

Blog Articles

60

External References

55

------------------------------------------------------------
AI DISPATCH AGENT RETRIEVAL
------------------------------------------------------------

Required Context

Current Jobs

Available Crews

Available Vehicles

Active Shipments

Service Requirements

Equipment Requirements

Graph Expansion

Depth = 2

------------------------------------------------------------
AI PRICING AGENT RETRIEVAL
------------------------------------------------------------

Required Context

Service Type

Cargo Type

Equipment Requirements

Distance

Risk Factors

Historical Estimates

Graph Expansion

Depth = 3

------------------------------------------------------------
AI ROUTING AGENT RETRIEVAL
------------------------------------------------------------

Required Context

Origin

Destination

Corridors

Ports

Current Workload

Vehicle Capacity

Graph Expansion

Depth = 3

------------------------------------------------------------
AI RISK AGENT RETRIEVAL
------------------------------------------------------------

Required Context

Shipment

Cargo

Equipment

Crew

Risk Categories

Incident History

Graph Expansion

Depth = 4

------------------------------------------------------------
VECTOR STORE INTEGRATION
------------------------------------------------------------

Embeddable Objects

Service

FAQ

Case Study

Workflow

Search Intent

Ontology Definition

Dataset Metadata

------------------------------------------------------------

Never Embed

Raw Events

Invoices

Internal Notes

Payment Data

Private Customer Information

------------------------------------------------------------
GRAPHRAG RETRIEVAL PIPELINE
------------------------------------------------------------

Query

↓

Intent Detection

↓

Entity Extraction

↓

Graph Search

↓

Neighborhood Expansion

↓

Ontology Expansion

↓

State Expansion

↓

Event Expansion

↓

Context Ranking

↓

LLM Prompt Assembly

↓

Response Generation

------------------------------------------------------------
GRAPHRAG PROMPT TEMPLATE
------------------------------------------------------------

System Context

Ontology

Current State

Recent Events

Graph Relationships

Historical Cases

Relevant FAQs

User Question

------------------------------------------------------------
SEARCH INTENT RETRIEVAL
------------------------------------------------------------

Example

Query:

Container Deconsolidation Virginia

Resolve:

Service:
Container Deconsolidation

Locations:
Virginia

Expand:

Port of Virginia

Virginia Inland Port

I-81

I-66

Warehouse Labor

Cross Docking

Transloading

Return:

Structured Context Package

------------------------------------------------------------
COMMERCIAL INTELLIGENCE RETRIEVAL
------------------------------------------------------------

Intent Categories

Transactional

Informational

Navigational

Operational

Emergency

Enterprise

------------------------------------------------------------

Example

"TWIC labor Port of Virginia"

Classification

Transactional

Priority Score

100

Graph Expansion

Port
↓
Service
↓
Organization

------------------------------------------------------------
LOGISTICS KNOWLEDGE PACKAGE FORMAT
------------------------------------------------------------

{
  "entity": {},
  "state": {},
  "events": [],
  "relationships": [],
  "ontology": [],
  "caseStudies": [],
  "faqs": [],
  "searchIntents": []
}

------------------------------------------------------------
GRAPHRAG OUTPUT CONTRACT
------------------------------------------------------------

Every retrieval response must contain:

Entity Context

Current State

Relevant Events

Graph Relationships

Ontology Definitions

Supporting Knowledge

Confidence Score

------------------------------------------------------------
SECURITY REQUIREMENTS
------------------------------------------------------------

Never expose:

Customer PII

Invoices

Payment Records

Internal Notes

Private Addresses

Credentials

Authentication Data

------------------------------------------------------------
SUPPORTED PLATFORMS
------------------------------------------------------------

Neo4j

Memgraph

Amazon Neptune

Azure Cosmos DB

GraphRAG

LlamaIndex

LangChain

OpenAI Retrieval

Claude Retrieval

Perplexity

Google AI Overviews

Knowledge Graph Systems

RDF Triple Stores

Vector Databases

------------------------------------------------------------
FUTURE EXPANSION
------------------------------------------------------------

Dispatch Agents

Pricing Agents

Routing Agents

Risk Agents

Inventory Agents

Warehouse Agents

Port Logistics Agents

Data Center Logistics Agents

Container Deconsolidation Agents

------------------------------------------------------------
END SPECIFICATION
------------------------------------------------------------
