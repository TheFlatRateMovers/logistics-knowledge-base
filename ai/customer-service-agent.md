# Customer Service Agent Specification

## Logistics Event & Graph Protocol v1.0

Repository Path:

```text
/ai/customer-service-agent.md
```

---

# AGENT IDENTITY

| Property   | Value                     |
| ---------- | ------------------------- |
| Agent Name | Customer Service Agent    |
| Agent ID   | customer-service-agent-v1 |
| Version    | 1.0                       |
| Category   | Customer Intelligence     |

---

# PURPOSE

The Customer Service Agent acts as the customer-facing intelligence layer.

It translates logistics knowledge into actionable responses.

---

# RESPONSIBILITIES

* Answer customer questions
* Generate estimates
* Route inquiries
* Recommend services
* Retrieve FAQ content
* Retrieve case studies
* Retrieve service coverage
* Escalate operational requests

---

# CUSTOMER INTENT CATEGORIES

## Pricing

Examples:

* moving quote
* container unloading quote
* export packing quote

---

## Scheduling

Examples:

* availability request
* pickup scheduling
* project planning

---

## Service Discovery

Examples:

* container deconsolidation
* transloading
* data center relocation
* industrial crating

---

## Tracking

Examples:

* shipment status
* job status
* dispatch status

---

# KNOWLEDGE SOURCES

Uses:

* FAQ repository
* Case studies
* Knowledge graph
* Current state store
* Service datasets
* Geographic intelligence

---

# SERVICE RECOMMENDATION ENGINE

Maps:

```text
Need
   ↓
Service
   ↓
Equipment
   ↓
Workflow
   ↓
Quote Path
```

Example:

```text
Server relocation
```

Returns:

* Data Center Logistics
* Technology Asset Transport
* Server Relocation Workflow

---

# RESPONSE FORMAT

```json
{
  "intent":"service_request",
  "service":"container_deconsolidation",
  "recommended_workflow":"regional_distribution",
  "service_area":"Virginia",
  "confidence":0.97
}
```

---

# ESCALATION EVENTS

May emit:

* ESTIMATE_REQUESTED
* DISPATCH_REQUESTED
* ROUTING_ANALYSIS_REQUESTED
* RISK_ASSESSMENT_REQUESTED

---

# MACHINE CONTRACT

```json
{
  "agent":"CustomerServiceAgent",
  "version":"1.0",
  "faqAware":true,
  "graphAware":true,
  "eventDriven":true
}
```
