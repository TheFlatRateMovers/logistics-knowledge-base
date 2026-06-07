# Logistics Event & Graph Protocol
# Cypher Query Library v1.0

Repository:
https://github.com/TheFlatRateMovers/logistics-knowledge-base

Purpose:
This document defines the canonical Neo4j query library for the
Logistics Event & Graph Protocol.

These queries serve as:

- GraphRAG retrieval templates
- AI dispatch agent tools
- AI pricing agent tools
- AI routing agent tools
- AI risk detection tools
- Operations dashboard queries
- Executive intelligence queries
- Knowledge graph exploration queries

=========================================================
GRAPH MODEL REFERENCE
=========================================================

Primary Node Labels

:Organization
:Customer
:Shipment
:Job
:Estimate
:Invoice
:Vehicle
:Crew
:Employee
:Equipment
:Location
:Port
:Corridor
:County
:City
:ZipCode
:Service
:LogisticsEvent
:SearchIntent

Primary Relationships

PROVIDES
REQUESTED_BY
ASSIGNED_TO
HANDLED_BY
OWNS
USES
ORIGIN
DESTINATION
LOCATED_IN
CONNECTED_TO
ACCESSIBLE_VIA
SUPPORTED_BY
AFFECTS
GENERATED_BY
MATCHES_SERVICE
TARGETS_LOCATION
TARGETS_PORT
TARGETS_CORRIDOR
TARGETS_ZIP

=========================================================
SECTION 1
SERVICE DISCOVERY QUERIES
=========================================================

---------------------------------------------------------
Find All Services
---------------------------------------------------------

MATCH (s:Service)
RETURN s.serviceName
ORDER BY s.serviceName;

---------------------------------------------------------
Find Organization Services
---------------------------------------------------------

MATCH (o:Organization)-[:PROVIDES]->(s:Service)
RETURN
o.name,
collect(s.serviceName) AS services;

---------------------------------------------------------
Find Service By Name
---------------------------------------------------------

MATCH (s:Service)
WHERE toLower(s.serviceName)
CONTAINS "container"
RETURN s;

=========================================================
SECTION 2
PORT INTELLIGENCE
=========================================================

---------------------------------------------------------
Services Supported By Port
---------------------------------------------------------

MATCH
(p:Port)-[:SUPPORTED_BY]->(s:Service)

RETURN
p.portName,
collect(s.serviceName);

---------------------------------------------------------
Ports Supporting Container Services
---------------------------------------------------------

MATCH
(p:Port)-[:SUPPORTED_BY]->(s:Service)

WHERE
s.serviceName IN [
"Container Loading",
"Container Unloading",
"Container Deconsolidation",
"Transloading"
]

RETURN
DISTINCT p.portName;

---------------------------------------------------------
Port Connectivity Map
---------------------------------------------------------

MATCH
(p1:Port)-[:CONNECTED_TO]->(p2:Port)

RETURN
p1.portName,
p2.portName;

=========================================================
SECTION 3
CORRIDOR INTELLIGENCE
=========================================================

---------------------------------------------------------
Counties Connected To I-81
---------------------------------------------------------

MATCH
(c:County)-[:CONNECTED_TO]->
(i:Corridor {corridorId:"I81"})

RETURN
c.countyName;

---------------------------------------------------------
Ports Accessible Through Corridor
---------------------------------------------------------

MATCH
(c:Corridor)-[:CONNECTS_TO]->
(p:Port)

RETURN
c.corridorName,
collect(p.portName);

---------------------------------------------------------
Service Coverage By Corridor
---------------------------------------------------------

MATCH
(c:Corridor)-[:CONNECTS_TO]->
(p:Port)-[:SUPPORTED_BY]->
(s:Service)

RETURN
c.corridorName,
collect(DISTINCT s.serviceName);

=========================================================
SECTION 4
GEOGRAPHIC RETRIEVAL
=========================================================

---------------------------------------------------------
ZIP → City → County Lookup
---------------------------------------------------------

MATCH
(z:ZipCode)-[:LOCATED_IN]->
(ci:City)-[:LOCATED_IN]->
(co:County)

RETURN
z.zipCode,
ci.cityName,
co.countyName;

---------------------------------------------------------
County Service Coverage
---------------------------------------------------------

MATCH
(co:County)<-[:LOCATED_IN]-
(ci:City)

MATCH
(ci)<-[:TARGETS_LOCATION]-
(si:SearchIntent)-[:MATCHES_SERVICE]->
(s:Service)

RETURN
co.countyName,
collect(DISTINCT s.serviceName);

---------------------------------------------------------
All Cities In County
---------------------------------------------------------

MATCH
(ci:City)-[:LOCATED_IN]->
(co:County)

RETURN
co.countyName,
collect(ci.cityName);

=========================================================
SECTION 5
SHIPMENT OPERATIONS
=========================================================

---------------------------------------------------------
Active Shipments
---------------------------------------------------------

MATCH
(s:Shipment)

WHERE
s.status IN [
"created",
"scheduled",
"assigned",
"in_transit"
]

RETURN s;

---------------------------------------------------------
Shipments In Transit
---------------------------------------------------------

MATCH
(s:Shipment)

WHERE
s.status = "in_transit"

RETURN
s.shipmentId,
s.originCity,
s.destinationCity;

---------------------------------------------------------
Shipment Equipment Requirements
---------------------------------------------------------

MATCH
(s:Shipment)-[:USES]->
(e:Equipment)

RETURN
s.shipmentId,
collect(e.equipmentType);

=========================================================
SECTION 6
JOB OPERATIONS
=========================================================

---------------------------------------------------------
Jobs By Status
---------------------------------------------------------

MATCH
(j:Job)

RETURN
j.status,
count(*);

---------------------------------------------------------
Open Jobs
---------------------------------------------------------

MATCH
(j:Job)

WHERE
j.status <> "completed"

RETURN j;

---------------------------------------------------------
Jobs Awaiting Vehicle Assignment
---------------------------------------------------------

MATCH
(j:Job)

WHERE
j.assignedVehicle IS NULL

RETURN
j.jobId,
j.status;

=========================================================
SECTION 7
VEHICLE INTELLIGENCE
=========================================================

---------------------------------------------------------
Available Vehicles
---------------------------------------------------------

MATCH
(v:Vehicle)

WHERE
v.status = "available"

RETURN v;

---------------------------------------------------------
Vehicle Utilization
---------------------------------------------------------

MATCH
(v:Vehicle)<-[:ASSIGNED_TO]-
(j:Job)

RETURN
v.vehicleId,
count(j) AS jobsAssigned;

---------------------------------------------------------
Underutilized Vehicles
---------------------------------------------------------

MATCH
(v:Vehicle)

OPTIONAL MATCH
(v)<-[:ASSIGNED_TO]-(j:Job)

RETURN
v.vehicleId,
count(j) AS assignmentCount
ORDER BY assignmentCount ASC;

=========================================================
SECTION 8
CREW INTELLIGENCE
=========================================================

---------------------------------------------------------
Crew Workload
---------------------------------------------------------

MATCH
(c:Crew)<-[:HANDLED_BY]-
(j:Job)

RETURN
c.crewId,
count(j);

---------------------------------------------------------
Idle Crews
---------------------------------------------------------

MATCH
(c:Crew)

WHERE
c.status = "available"

RETURN c;

---------------------------------------------------------
Crew Capacity Utilization
---------------------------------------------------------

MATCH
(c:Crew)

RETURN
c.crewId,
c.currentAssignments,
c.maxAssignments;

=========================================================
SECTION 9
EVENT STREAM ANALYTICS
=========================================================

---------------------------------------------------------
Events By Type
---------------------------------------------------------

MATCH
(e:LogisticsEvent)

RETURN
e.eventType,
count(*);

---------------------------------------------------------
Recent Events
---------------------------------------------------------

MATCH
(e:LogisticsEvent)

RETURN
e
ORDER BY e.timestamp DESC
LIMIT 100;

---------------------------------------------------------
Events Affecting Shipment
---------------------------------------------------------

MATCH
(e:LogisticsEvent)-[:AFFECTS]->
(s:Shipment)

WHERE
s.shipmentId = $shipmentId

RETURN
e
ORDER BY e.timestamp;

=========================================================
SECTION 10
EVENT CHAIN RECONSTRUCTION
=========================================================

---------------------------------------------------------
Full Shipment Timeline
---------------------------------------------------------

MATCH
(e:LogisticsEvent)-[:AFFECTS]->
(s:Shipment)

WHERE
s.shipmentId = $shipmentId

RETURN
e.eventType,
e.timestamp
ORDER BY e.timestamp;

---------------------------------------------------------
Job Lifecycle
---------------------------------------------------------

MATCH
(e:LogisticsEvent)-[:AFFECTS]->
(j:Job)

WHERE
j.jobId = $jobId

RETURN
e.eventType,
e.timestamp
ORDER BY e.timestamp;

=========================================================
SECTION 11
AI RETRIEVAL QUERIES
=========================================================

---------------------------------------------------------
Find Services For Search Intent
---------------------------------------------------------

MATCH
(si:SearchIntent)-[:MATCHES_SERVICE]->
(s:Service)

RETURN
si.intentText,
s.serviceName;

---------------------------------------------------------
Find Relevant Service Areas
---------------------------------------------------------

MATCH
(si:SearchIntent)-[:TARGETS_ZIP]->
(z:ZipCode)

RETURN
si.intentText,
collect(z.zipCode);

---------------------------------------------------------
AI Recommendation Query
---------------------------------------------------------

MATCH
(si:SearchIntent)-[:MATCHES_SERVICE]->
(s:Service)

MATCH
(s)<-[:PROVIDES]-
(o:Organization)

RETURN
si.intentText,
s.serviceName,
o.name;

=========================================================
SECTION 12
GRAPH RAG QUERIES
=========================================================

---------------------------------------------------------
Neighborhood Expansion Query
---------------------------------------------------------

MATCH (n)
WHERE id(n) = $nodeId

MATCH (n)-[r]-(m)

RETURN
n,
r,
m;

---------------------------------------------------------
2-Hop Context Expansion
---------------------------------------------------------

MATCH (n)
WHERE id(n) = $nodeId

MATCH path =
(n)-[*1..2]-(m)

RETURN path;

---------------------------------------------------------
Service Knowledge Context
---------------------------------------------------------

MATCH
(s:Service {serviceName:$service})

MATCH path =
(s)-[*1..3]-(related)

RETURN path;

=========================================================
SECTION 13
RISK DETECTION
=========================================================

---------------------------------------------------------
Delayed Jobs
---------------------------------------------------------

MATCH
(j:Job)

WHERE
j.status = "delayed"

RETURN j;

---------------------------------------------------------
High-Risk Shipments
---------------------------------------------------------

MATCH
(s:Shipment)

WHERE
s.riskLevel IN [
"high",
"critical"
]

RETURN s;

---------------------------------------------------------
Equipment Constraints
---------------------------------------------------------

MATCH
(s:Shipment)-[:USES]->
(e:Equipment)

WHERE
e.requiresCertification = true

RETURN
s.shipmentId,
e.equipmentType;

=========================================================
SECTION 14
EXECUTIVE DASHBOARD
=========================================================

---------------------------------------------------------
Daily Operations Summary
---------------------------------------------------------

MATCH (j:Job)

RETURN
count(j) AS totalJobs,
count(
CASE
WHEN j.status='completed'
THEN 1
END
) AS completedJobs;

---------------------------------------------------------
Revenue Snapshot
---------------------------------------------------------

MATCH
(i:Invoice)

RETURN
sum(i.totalAmount) AS revenue;

---------------------------------------------------------
Service Demand Ranking
---------------------------------------------------------

MATCH
(j:Job)-[:USES_SERVICE]->
(s:Service)

RETURN
s.serviceName,
count(j) AS demand
ORDER BY demand DESC;

=========================================================
SECTION 15
FUTURE AGENT INTERFACES
=========================================================

Dispatch Agent

- Available crews
- Available vehicles
- Open jobs
- Travel distance

Pricing Agent

- Service type
- Shipment complexity
- Equipment requirements

Routing Agent

- Corridor congestion
- Vehicle availability
- Delivery deadlines

Risk Agent

- Delays
- Equipment conflicts
- Regulatory constraints

=========================================================
END OF SPECIFICATION
=========================================================
