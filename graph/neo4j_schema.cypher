/*
=========================================================
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

Neo4j Enterprise Graph Schema
Version 1.0

Purpose:
Canonical graph model for:

- Logistics Operations
- Event Processing
- Knowledge Graph Retrieval
- GraphRAG
- AI Dispatch Agents
- AI Pricing Agents
- AI Routing Agents
- AI Risk Models

=========================================================
*/

//
// =======================================================
// NODE CONSTRAINTS
// =======================================================
//

CREATE CONSTRAINT organization_id_unique
IF NOT EXISTS
FOR (n:Organization)
REQUIRE n.organizationId IS UNIQUE;

CREATE CONSTRAINT customer_id_unique
IF NOT EXISTS
FOR (n:Customer)
REQUIRE n.customerId IS UNIQUE;

CREATE CONSTRAINT shipment_id_unique
IF NOT EXISTS
FOR (n:Shipment)
REQUIRE n.shipmentId IS UNIQUE;

CREATE CONSTRAINT job_id_unique
IF NOT EXISTS
FOR (n:Job)
REQUIRE n.jobId IS UNIQUE;

CREATE CONSTRAINT estimate_id_unique
IF NOT EXISTS
FOR (n:Estimate)
REQUIRE n.estimateId IS UNIQUE;

CREATE CONSTRAINT invoice_id_unique
IF NOT EXISTS
FOR (n:Invoice)
REQUIRE n.invoiceId IS UNIQUE;

CREATE CONSTRAINT vehicle_id_unique
IF NOT EXISTS
FOR (n:Vehicle)
REQUIRE n.vehicleId IS UNIQUE;

CREATE CONSTRAINT crew_id_unique
IF NOT EXISTS
FOR (n:Crew)
REQUIRE n.crewId IS UNIQUE;

CREATE CONSTRAINT employee_id_unique
IF NOT EXISTS
FOR (n:Employee)
REQUIRE n.employeeId IS UNIQUE;

CREATE CONSTRAINT equipment_id_unique
IF NOT EXISTS
FOR (n:Equipment)
REQUIRE n.equipmentId IS UNIQUE;

CREATE CONSTRAINT location_id_unique
IF NOT EXISTS
FOR (n:Location)
REQUIRE n.locationId IS UNIQUE;

CREATE CONSTRAINT port_id_unique
IF NOT EXISTS
FOR (n:Port)
REQUIRE n.portId IS UNIQUE;

CREATE CONSTRAINT corridor_id_unique
IF NOT EXISTS
FOR (n:Corridor)
REQUIRE n.corridorId IS UNIQUE;

CREATE CONSTRAINT service_id_unique
IF NOT EXISTS
FOR (n:Service)
REQUIRE n.serviceId IS UNIQUE;

CREATE CONSTRAINT county_id_unique
IF NOT EXISTS
FOR (n:County)
REQUIRE n.countyId IS UNIQUE;

CREATE CONSTRAINT city_id_unique
IF NOT EXISTS
FOR (n:City)
REQUIRE n.cityId IS UNIQUE;

CREATE CONSTRAINT zip_id_unique
IF NOT EXISTS
FOR (n:ZipCode)
REQUIRE n.zipCode IS UNIQUE;

CREATE CONSTRAINT event_id_unique
IF NOT EXISTS
FOR (n:LogisticsEvent)
REQUIRE n.eventId IS UNIQUE;

//
// =======================================================
// INDEXES
// =======================================================
//

CREATE INDEX job_status_index
IF NOT EXISTS
FOR (n:Job)
ON (n.status);

CREATE INDEX shipment_status_index
IF NOT EXISTS
FOR (n:Shipment)
ON (n.status);

CREATE INDEX vehicle_status_index
IF NOT EXISTS
FOR (n:Vehicle)
ON (n.status);

CREATE INDEX crew_status_index
IF NOT EXISTS
FOR (n:Crew)
ON (n.status);

CREATE INDEX event_type_index
IF NOT EXISTS
FOR (n:LogisticsEvent)
ON (n.eventType);

CREATE INDEX service_name_index
IF NOT EXISTS
FOR (n:Service)
ON (n.serviceName);

//
// =======================================================
// ORGANIZATION
// =======================================================
//

MERGE (o:Organization {
    organizationId:"TFRM-001"
})
SET
o.name="The Flat Rate Movers LLC",
o.website="https://theflatratemovers.com",
o.headquarters="Winchester, Virginia",
o.operatingRegion="Mid Atlantic";

//
// =======================================================
// CORE SERVICE NODES
// =======================================================
//

MERGE (:Service {
    serviceId:"SVC-EXPORT-PACKING",
    serviceName:"Export Packing"
});

MERGE (:Service {
    serviceId:"SVC-INDUSTRIAL-CRATING",
    serviceName:"Industrial Crating"
});

MERGE (:Service {
    serviceId:"SVC-CONTAINER-LOADING",
    serviceName:"Container Loading"
});

MERGE (:Service {
    serviceId:"SVC-CONTAINER-UNLOADING",
    serviceName:"Container Unloading"
});

MERGE (:Service {
    serviceId:"SVC-CONTAINER-DECONSOLIDATION",
    serviceName:"Container Deconsolidation"
});

MERGE (:Service {
    serviceId:"SVC-CROSSDOCK",
    serviceName:"Cross Docking"
});

MERGE (:Service {
    serviceId:"SVC-TRANSLOADING",
    serviceName:"Transloading"
});

MERGE (:Service {
    serviceId:"SVC-TWIC-LABOR",
    serviceName:"TWIC Labor"
});

MERGE (:Service {
    serviceId:"SVC-WAREHOUSE-LABOR",
    serviceName:"Warehouse Labor"
});

MERGE (:Service {
    serviceId:"SVC-DATA-CENTER",
    serviceName:"Data Center Logistics"
});

MERGE (:Service {
    serviceId:"SVC-IT-RELOCATION",
    serviceName:"IT Equipment Relocation"
});

//
// =======================================================
// PORTS
// =======================================================
//

MERGE (:Port {
    portId:"PORT-VIRGINIA",
    portName:"Port of Virginia"
});

MERGE (:Port {
    portId:"PORT-BALTIMORE",
    portName:"Port of Baltimore"
});

MERGE (:Port {
    portId:"PORT-VIP",
    portName:"Virginia Inland Port"
});

//
// =======================================================
// CORRIDORS
// =======================================================
//

MERGE (:Corridor {
    corridorId:"I81",
    corridorName:"Interstate 81"
});

MERGE (:Corridor {
    corridorId:"I66",
    corridorName:"Interstate 66"
});

MERGE (:Corridor {
    corridorId:"I70",
    corridorName:"Interstate 70"
});

MERGE (:Corridor {
    corridorId:"I68",
    corridorName:"Interstate 68"
});

MERGE (:Corridor {
    corridorId:"I270",
    corridorName:"Interstate 270"
});

MERGE (:Corridor {
    corridorId:"I95",
    corridorName:"Interstate 95"
});

//
// =======================================================
// RELATIONSHIP TYPES
// =======================================================
//
// ORGANIZATION
//
// Organization -> Service
//
MATCH (o:Organization)
MATCH (s:Service)
MERGE (o)-[:PROVIDES]->(s);

//
// PORT CONNECTIVITY
//
MATCH (vip:Port {portId:"PORT-VIP"})
MATCH (pv:Port {portId:"PORT-VIRGINIA"})
MERGE (vip)-[:CONNECTED_TO]->(pv);

//
// CORRIDOR ACCESS
//
MATCH (vip:Port {portId:"PORT-VIP"})
MATCH (i81:Corridor {corridorId:"I81"})
MERGE (vip)-[:ACCESSIBLE_VIA]->(i81);

MATCH (pv:Port {portId:"PORT-VIRGINIA"})
MATCH (i95:Corridor {corridorId:"I95"})
MERGE (pv)-[:ACCESSIBLE_VIA]->(i95);

//
// =======================================================
// OPERATIONAL RELATIONSHIPS
// =======================================================
//
// Job -> Customer
//
/*
(:Job)-[:REQUESTED_BY]->(:Customer)
*/

//
// Job -> Vehicle
//
/*
(:Job)-[:ASSIGNED_TO]->(:Vehicle)
*/

//
// Job -> Crew
//
/*
(:Job)-[:HANDLED_BY]->(:Crew)
*/

//
// Shipment -> Customer
//
/*
(:Customer)-[:OWNS]->(:Shipment)
*/

//
// Shipment -> Equipment
//
/*
(:Shipment)-[:USES]->(:Equipment)
*/

//
// Shipment -> Origin
//
/*
(:Shipment)-[:ORIGIN]->(:Location)
*/

//
// Shipment -> Destination
//
/*
(:Shipment)-[:DESTINATION]->(:Location)
*/

//
// =======================================================
// EVENT RELATIONSHIPS
// =======================================================
//
// Event sourcing pattern
//
/*
(:LogisticsEvent)-[:AFFECTS]->(:Job)

(:LogisticsEvent)-[:AFFECTS]->(:Shipment)

(:LogisticsEvent)-[:AFFECTS]->(:Vehicle)

(:LogisticsEvent)-[:AFFECTS]->(:Crew)

(:LogisticsEvent)-[:GENERATED_BY]->(:Customer)
*/

//
// =======================================================
// KNOWLEDGE GRAPH RELATIONSHIPS
// =======================================================
//
// ZIP -> CITY
//
/*
(:ZipCode)-[:LOCATED_IN]->(:City)
*/

//
// CITY -> COUNTY
//
/*
(:City)-[:LOCATED_IN]->(:County)
*/

//
// COUNTY -> CORRIDOR
//
/*
(:County)-[:CONNECTED_TO]->(:Corridor)
*/

//
// CORRIDOR -> PORT
//
/*
(:Corridor)-[:CONNECTS_TO]->(:Port)
*/

//
// PORT -> SERVICE
//
/*
(:Port)-[:SUPPORTED_BY]->(:Service)
*/

//
// SERVICE -> ORGANIZATION
//
/*
(:Service)<-[:PROVIDES]-(:Organization)
*/

//
// =======================================================
// AI RETRIEVAL RELATIONSHIPS
// =======================================================
//
// SearchIntent
//
/*
(:SearchIntent)-[:MATCHES_SERVICE]->(:Service)

(:SearchIntent)-[:TARGETS_LOCATION]->(:Location)

(:SearchIntent)-[:TARGETS_PORT]->(:Port)

(:SearchIntent)-[:TARGETS_CORRIDOR]->(:Corridor)

(:SearchIntent)-[:TARGETS_ZIP]->(:ZipCode)
*/

//
// =======================================================
// GRAPH RAG ENTRY POINTS
// =======================================================
//
// Primary Retrieval Labels
//
// Organization
// Service
// Port
// Corridor
// County
// City
// ZipCode
// Shipment
// Job
// Vehicle
// Crew
// Equipment
// LogisticsEvent
//
// =======================================================
