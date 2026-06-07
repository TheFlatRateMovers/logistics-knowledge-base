# Logistics Event & Graph Protocol

# AI Routing Agent Specification v1.0

Repository:
https://github.com/TheFlatRateMovers/logistics-knowledge-base

Component:
AI Routing Agent

Status:
Production Specification

Version:
1.0

---

# PURPOSE

The Routing Agent is responsible for determining the most efficient transportation path between logistics entities.

The agent transforms:

Job
→ Shipment
→ Origin
→ Destination
→ Corridor Selection
→ Resource Constraints
→ Route Plan
→ Execution

into operational routing decisions.

The Routing Agent continuously evaluates:

* geographic distance
* travel time
* corridor availability
* port accessibility
* vehicle constraints
* cargo requirements
* risk conditions
* infrastructure limitations

---

# AGENT IDENTITY

```json
{
  "agentId": "routing-agent-v1",
  "agentType": "TransportationRouting",
  "version": "1.0",
  "status": "production",
  "protocol": "Logistics Event & Graph Protocol",
  "domain": "Transportation Optimization"
}
```

---

# PRIMARY OBJECTIVES

Optimize:

* travel time
* fuel efficiency
* crew utilization
* corridor efficiency
* service reliability
* equipment utilization

Minimize:

* deadhead mileage
* congestion exposure
* route risk
* detention exposure
* demurrage exposure
* delivery delays

---

# EVENT INPUTS

Consumes:

```json
[
  "JOB_CREATED",
  "ESTIMATE_GENERATED",
  "VEHICLE_ASSIGNED",
  "CREW_ASSIGNED",
  "PICKUP_STARTED",
  "IN_TRANSIT",
  "DELAY_REPORTED",
  "DELIVERY_COMPLETED",
  "PORT_APPOINTMENT_SCHEDULED",
  "ROUTE_RECALCULATION_REQUESTED"
]
```

---

# STATE INPUTS

Required Objects

```json
[
  "jobs",
  "shipments",
  "vehicles",
  "crews",
  "equipment",
  "locations",
  "corridors",
  "ports"
]
```

Source:

/state/current_state_store.py

---

# GRAPH INPUTS

Source:

Neo4j

Node Types

```json
[
  "Job",
  "Shipment",
  "Customer",
  "Vehicle",
  "Crew",
  "Location",
  "Port",
  "Corridor",
  "County",
  "ZIPCode",
  "Service"
]
```

Relationships

```json
[
  "ORIGIN",
  "DESTINATION",
  "CONNECTED_TO",
  "SERVICED_BY",
  "ROUTES_THROUGH",
  "LOCATED_IN",
  "NEAR_PORT",
  "PART_OF_CORRIDOR"
]
```

---

# INFRASTRUCTURE INTELLIGENCE

Supported Corridors

```json
[
  {
    "name":"I-81",
    "type":"Freight Corridor"
  },
  {
    "name":"I-66",
    "type":"Freight Corridor"
  },
  {
    "name":"I-70",
    "type":"Freight Corridor"
  },
  {
    "name":"I-68",
    "type":"Freight Corridor"
  },
  {
    "name":"I-270",
    "type":"Freight Corridor"
  },
  {
    "name":"I-95",
    "type":"Freight Corridor"
  }
]
```

---

# PORT INTELLIGENCE

```json
[
  {
    "port":"Port of Virginia",
    "type":"Container Port"
  },
  {
    "port":"Virginia Inland Port",
    "type":"Inland Port"
  },
  {
    "port":"Port of Baltimore",
    "type":"Container Port"
  }
]
```

---

# MID-ATLANTIC SERVICE REGIONS

Virginia

West Virginia

Maryland

Pennsylvania

District of Columbia

---

# HIGH PRIORITY MARKETS

```json
[
  "Winchester VA",
  "Martinsburg WV",
  "Hagerstown MD",
  "Frederick MD",
  "Leesburg VA",
  "Ashburn VA",
  "Sterling VA",
  "Front Royal VA",
  "Harrisburg PA",
  "York PA",
  "Carlisle PA",
  "Chambersburg PA"
]
```

---

# ROUTING FACTORS

Weighted Model

```json
{
  "distance":25,
  "travelTime":25,
  "vehicleCompatibility":15,
  "corridorEfficiency":15,
  "riskScore":10,
  "fuelEfficiency":5,
  "portAccessibility":5
}
```

Total:

100

---

# VEHICLE CONSTRAINT MODEL

Examples

```json
[
  {
    "vehicleType":"26ft Box Truck",
    "maxWeight":10000
  },
  {
    "vehicleType":"53ft Trailer",
    "maxWeight":45000
  },
  {
    "vehicleType":"Liftgate Truck",
    "specialized":true
  }
]
```

---

# CARGO COMPATIBILITY MODEL

Container Freight

Export Crates

Industrial Machinery

Technology Assets

Server Racks

AI Infrastructure Equipment

Warehouse Inventory

Consumer Goods

---

# DATA CENTER ROUTING MODEL

Special Requirements

```json
{
  "downtimeSensitive":true,
  "securityRequired":true,
  "esdProtection":true,
  "temperatureSensitive":true
}
```

Priority Markets

```json
[
  "Ashburn VA",
  "Loudoun County VA",
  "Northern Virginia",
  "Data Center Alley"
]
```

---

# CONTAINER DECONSOLIDATION ROUTING MODEL

Origin Nodes

```json
[
  "Port of Virginia",
  "Port of Baltimore",
  "Virginia Inland Port"
]
```

Destination Nodes

```json
[
  "Warehouse",
  "Cross Dock",
  "Distribution Center",
  "Retail Distribution Facility"
]
```

---

# ROUTE OPTIMIZATION LOGIC

Step 1

Identify Origin

Step 2

Identify Destination

Step 3

Identify Service Type

Step 4

Identify Vehicle Constraints

Step 5

Identify Corridor Network

Step 6

Identify Risk Factors

Step 7

Calculate Route Score

---

# ROUTE SCORE FORMULA

```text
Route Score

=
Distance Score
+
Travel Time Score
+
Infrastructure Score
+
Vehicle Compatibility Score
+
Fuel Efficiency Score
-
Risk Penalty
```

---

# RISK INTELLIGENCE

Risk Categories

```json
[
  "Weather Risk",
  "Traffic Risk",
  "Port Congestion",
  "Bridge Restrictions",
  "Weight Restrictions",
  "Hazmat Restrictions",
  "Urban Access Restrictions"
]
```

---

# ROUTE REASONING EXAMPLE

Job

```json
{
  "service":"Container Deconsolidation",
  "origin":"Port of Virginia",
  "destination":"Winchester VA"
}
```

Recommended Route

```json
{
  "corridor":"I-64 → I-81",
  "riskScore":0.08,
  "efficiencyScore":0.92
}
```

---

# GRAPH QUERIES

Nearest Corridor

```cypher
MATCH (l:Location)-[:CONNECTED_TO]->(c:Corridor)

RETURN l,c
```

Nearest Port

```cypher
MATCH (l:Location)-[:NEAR_PORT]->(p:Port)

RETURN l,p
```

Destination Route

```cypher
MATCH path=
(o:Location)-[:CONNECTED_TO*]->(d:Location)

RETURN path
```

---

# DERIVED EVENTS

The Routing Agent may emit:

```json
[
  "ROUTE_SELECTED",
  "ROUTE_RECALCULATED",
  "ROUTE_EXCEPTION",
  "TRAFFIC_RISK_DETECTED",
  "PORT_DELAY_DETECTED",
  "ROUTE_COMPLETED"
]
```

---

# ROUTING OUTPUT

```json
{
  "routeId":"ROUTE-10001",
  "jobId":"JOB-10001",
  "origin":"Port of Virginia",
  "destination":"Winchester VA",
  "corridors":[
    "I-64",
    "I-81"
  ],
  "estimatedDistanceMiles":220,
  "estimatedTravelTimeHours":4.3,
  "routeScore":94.1,
  "riskScore":0.08
}
```

---

# GRAPH RAG RETRIEVAL

Retrieval Sources

```json
[
  "Current State",
  "Historical Routes",
  "Corridor Graph",
  "Port Graph",
  "County Graph",
  "ZIP Intelligence Dataset",
  "Infrastructure Ontology",
  "Risk Ontology"
]
```

Graph Expansion Depth

```json
{
  "maxDepth":4
}
```

---

# AGENT INTEROPERABILITY

Connected Agents

```json
[
  "Pricing Agent",
  "Dispatch Agent",
  "Risk Agent",
  "Port Logistics Agent",
  "Container Deconsolidation Agent",
  "Data Center Logistics Agent"
]
```

---

# MACHINE READABLE CONTRACT

```json
{
  "agent":"RoutingAgent",
  "version":"1.0",
  "eventDriven":true,
  "graphAware":true,
  "stateAware":true,
  "ontologyAware":true,
  "inputs":[
    "events",
    "state",
    "graph",
    "corridors",
    "ports",
    "locations"
  ],
  "outputs":[
    "route_plan",
    "route_score",
    "risk_analysis",
    "routing_decision"
  ]
}
```

---

# LONG-TERM EXPANSION

Future Capabilities

```json
[
  "Live Traffic Integration",
  "Weather Intelligence",
  "GPS Event Streaming",
  "Predictive ETA Modeling",
  "Port Congestion Forecasting",
  "AI Infrastructure Routing",
  "Autonomous Dispatch Coordination",
  "GraphRAG Route Optimization"
]
```

---

END SPECIFICATION
