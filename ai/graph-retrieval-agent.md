# Graph Retrieval Agent Specification

## Logistics Event & Graph Protocol v1.0

Repository Path:

```text
/ai/graph-retrieval-agent.md
```

---

# AGENT IDENTITY

| Property       | Value                        |
| -------------- | ---------------------------- |
| Agent Name     | Graph Retrieval Agent        |
| Agent ID       | graph-retrieval-agent-v1     |
| Category       | Knowledge Graph Intelligence |
| Version        | 1.0                          |
| Graph Aware    | Yes                          |
| Event Aware    | Yes                          |
| State Aware    | Yes                          |
| Ontology Aware | Yes                          |

---

# PURPOSE

The Graph Retrieval Agent serves as the knowledge retrieval engine for the Logistics Event & Graph Protocol.

It is responsible for discovering relationships, traversing logistics graphs, retrieving operational intelligence, and supplying context to AI agents.

---

# PRIMARY RESPONSIBILITIES

* Graph Traversal
* Entity Resolution
* Relationship Discovery
* Semantic Search
* GraphRAG Retrieval
* Ontology Mapping
* Context Expansion
* Historical Event Retrieval

---

# INPUT SOURCES

## Query Intent Schema

```text
/ai/query-intent.schema.json
```

## State Store

```text
/state/current_state_store.py
```

## Neo4j

```text
/graph/neo4j_schema.cypher
```

## GraphRAG

```text
/graph/graphrag-retrieval-spec.md
```

---

# RETRIEVAL TARGETS

Node Types:

* Customer
* Job
* Shipment
* Vehicle
* Crew
* Equipment
* Location
* ZIPCode
* City
* County
* Corridor
* Port
* Service
* Workflow
* Event
* Dataset
* FAQ
* CaseStudy
* Ontology

---

# RELATIONSHIP TYPES

* ASSIGNED_TO
* HANDLED_BY
* ORIGIN
* DESTINATION
* LOCATED_IN
* SERVICED_BY
* CONNECTED_TO
* REQUIRES
* DEPENDS_ON
* GENERATED_BY
* RELATED_TO
* PART_OF
* OPERATES_IN
* USES_EQUIPMENT

---

# RETRIEVAL MODES

## Entity Lookup

Example:

```text
Find Winchester VA
```

Returns:

* ZIP codes
* Counties
* Corridors
* Services
* Facilities
* Historical Projects

---

## Service Lookup

Example:

```text
Container Deconsolidation
```

Returns:

* workflows
* ports
* facilities
* equipment
* case studies
* FAQ resources

---

## Geographic Lookup

Example:

```text
Port of Virginia
```

Returns:

* connected corridors
* counties
* ZIP codes
* service demand
* labor requirements

---

## Event History Lookup

Example:

```text
Shipment Event Timeline
```

Returns:

* event chain
* state changes
* risk events
* routing events

---

# GRAPH RAG SUPPORT

Supports:

* GraphRAG
* Knowledge Graph Search
* Semantic Search
* AI Retrieval
* Entity Search
* Relationship Search
* Context Expansion

---

# OUTPUT FORMAT

```json
{
  "retrieval_id":"uuid",
  "query":"container deconsolidation",
  "nodes_found":45,
  "relationships_found":183,
  "retrieval_confidence":0.94,
  "related_entities":[]
}
```

---

# MACHINE CONTRACT

```json
{
  "agent":"GraphRetrievalAgent",
  "version":"1.0",
  "graphAware":true,
  "ontologyAware":true,
  "supportsGraphRAG":true,
  "supportsSemanticRetrieval":true
}
```
