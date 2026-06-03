# Graph Projection Rules

Purpose:

Convert logistics events into graph relationships.

Example:

JOB_CREATED

Customer -> Shipment

VEHICLE_ASSIGNED

Vehicle -> Shipment

DELIVERY_COMPLETED

Shipment -> Destination

Projection Process:

1. Read event stream
2. Identify participating entities
3. Create graph nodes
4. Create graph edges
5. Attach event metadata to edges
