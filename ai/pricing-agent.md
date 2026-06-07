# Logistics Event & Graph Protocol
# AI Pricing Agent Specification v1.0

Repository:
https://github.com/TheFlatRateMovers/logistics-knowledge-base

Component:
AI Pricing Agent

Status:
Production Specification

Version:
1.0

----------------------------------------------------------
PURPOSE
----------------------------------------------------------

The Pricing Agent is responsible for generating:

- Budgetary Estimates
- Formal Quotes
- Operational Pricing
- Risk Adjustments
- Labor Cost Modeling
- Equipment Cost Modeling
- Freight Handling Cost Modeling

The agent converts:

Customer Intent
    ↓
Service Requirements
    ↓
Operational Complexity
    ↓
Pricing Intelligence
    ↓
Estimate

----------------------------------------------------------
AGENT IDENTITY
----------------------------------------------------------

{
  "agentId":"pricing-agent-v1",
  "agentType":"OperationalPricing",
  "version":"1.0",
  "protocol":"Logistics Event & Graph Protocol",
  "domain":"Commercial Pricing"
}

----------------------------------------------------------
PRIMARY OBJECTIVE
----------------------------------------------------------

Optimize:

- Pricing Accuracy
- Quote Speed
- Margin Protection
- Resource Allocation
- Revenue Forecasting

Minimize:

- Underpricing
- Overpricing
- Margin Leakage
- Scope Errors

----------------------------------------------------------
EVENT INPUTS
----------------------------------------------------------

Consumes:

[
  "JOB_CREATED",
  "ESTIMATE_REQUESTED",
  "ESTIMATE_GENERATED",
  "SERVICE_SCOPE_UPDATED",
  "CREW_ASSIGNED",
  "VEHICLE_ASSIGNED",
  "RISK_DETECTED"
]

----------------------------------------------------------
STATE INPUTS
----------------------------------------------------------

Required Objects

[
  "jobs",
  "shipments",
  "customers",
  "locations",
  "vehicles",
  "crews",
  "equipment"
]

----------------------------------------------------------
GRAPH INPUTS
----------------------------------------------------------

Node Types

[
  "Customer",
  "Shipment",
  "Job",
  "Service",
  "Location",
  "Equipment",
  "Vehicle",
  "Crew",
  "RiskCategory",
  "Corridor",
  "Port"
]

----------------------------------------------------------
SERVICE CATEGORIES
----------------------------------------------------------

Residential Moving

Commercial Moving

Office Relocation

IT Equipment Relocation

Data Center Relocation

Industrial Relocation

Export Packing

Industrial Crating

Container Loading

Container Unloading

Container Deconsolidation

Cross Docking

Transloading

TWIC Labor

Warehouse Labor

Port Logistics

----------------------------------------------------------
PRICING DIMENSIONS
----------------------------------------------------------

{
  "labor":30,
  "distance":20,
  "equipment":15,
  "serviceComplexity":15,
  "risk":10,
  "urgency":10
}

Total = 100

----------------------------------------------------------
LABOR MODEL
----------------------------------------------------------

Inputs

Crew Size

Crew Experience

Crew Certifications

Estimated Hours

Formula

Labor Cost

=
Crew Count
×
Hourly Rate
×
Estimated Hours

----------------------------------------------------------
DISTANCE MODEL
----------------------------------------------------------

Inputs

Origin

Destination

Mileage

Travel Time

Corridor

Formula

Distance Cost

=
Mileage
×
Mileage Rate

----------------------------------------------------------
EQUIPMENT MODEL
----------------------------------------------------------

Equipment Types

Forklift

Pallet Jack

Container Ramp

Liftgate

Crane

Server Cart

Rack Lift

ESD Equipment

Rigging Equipment

Machine Skates

Hydraulic Gantry

Pricing Logic

Daily Rate

+
Mobilization Cost

+
Operator Cost

----------------------------------------------------------
SERVICE COMPLEXITY MODEL
----------------------------------------------------------

Low

1.0

Medium

1.25

High

1.50

Critical

2.0

----------------------------------------------------------
RISK FACTORS
----------------------------------------------------------

Cargo Damage Risk

Operational Risk

Weather Risk

Access Risk

Port Delay Risk

Schedule Risk

Technology Asset Risk

Data Center Risk

----------------------------------------------------------
RISK MULTIPLIERS
----------------------------------------------------------

{
  "low":1.00,
  "moderate":1.10,
  "high":1.25,
  "critical":1.50
}

----------------------------------------------------------
DATA CENTER LOGISTICS MODEL
----------------------------------------------------------

Factors

Server Quantity

Rack Quantity

Weight

Security Requirements

Downtime Constraints

ESD Requirements

Redundancy Requirements

----------------------------------------------------------
CONTAINER DECONSOLIDATION MODEL
----------------------------------------------------------

Factors

Container Type

Floor Loaded

Palletized

SKU Count

Sort Complexity

Redistribution Requirements

Warehouse Requirements

Cross Dock Requirements

----------------------------------------------------------
PORT LOGISTICS MODEL
----------------------------------------------------------

Factors

TWIC Labor

Terminal Access

Appointment Scheduling

Demurrage Risk

Detention Risk

Container Size

----------------------------------------------------------
GEOGRAPHIC MODEL
----------------------------------------------------------

Primary Markets

Winchester VA

Martinsburg WV

Ashburn VA

Leesburg VA

Hagerstown MD

Frederick MD

Harrisburg PA

York PA

----------------------------------------------------------
CORRIDOR INTELLIGENCE
----------------------------------------------------------

I-81

I-66

I-70

I-68

I-270

I-95

----------------------------------------------------------
PORT INTELLIGENCE
----------------------------------------------------------

Port of Virginia

Virginia Inland Port

Port of Baltimore

----------------------------------------------------------
ESTIMATE OUTPUT
----------------------------------------------------------

{
  "estimateId":"EST-1001",
  "serviceType":"Container Deconsolidation",
  "estimatedLabor":4500,
  "estimatedEquipment":1200,
  "estimatedTravel":700,
  "estimatedRiskAdjustment":600,
  "totalEstimate":7000,
  "confidenceScore":0.94
}

----------------------------------------------------------
PRICING CONFIDENCE MODEL
----------------------------------------------------------

Inputs

Historical Similar Jobs

Data Completeness

Risk Certainty

Route Certainty

Equipment Availability

Output

0.00 - 1.00

----------------------------------------------------------
DERIVED EVENTS
----------------------------------------------------------

[
  "ESTIMATE_GENERATED",
  "QUOTE_GENERATED",
  "QUOTE_UPDATED",
  "PRICING_EXCEPTION",
  "RISK_ADJUSTMENT_APPLIED"
]

----------------------------------------------------------
GRAPH RAG RETRIEVAL
----------------------------------------------------------

Required Context

Current State

Historical Jobs

Historical Estimates

Risk Categories

Service Ontology

Equipment Ontology

Cargo Ontology

----------------------------------------------------------
MACHINE READABLE CONTRACT
----------------------------------------------------------

{
  "agent":"PricingAgent",
  "version":"1.0",
  "eventDriven":true,
  "graphAware":true,
  "stateAware":true,
  "inputs":[
    "events",
    "state",
    "graph",
    "ontology"
  ],
  "outputs":[
    "estimate",
    "quote",
    "pricing_decision"
  ]
}

----------------------------------------------------------
END SPECIFICATION
----------------------------------------------------------
