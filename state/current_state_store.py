#!/usr/bin/env python3

"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

current_state_store.py

Purpose

Authoritative operational state store.

Converts immutable event history into
current operational reality.

This file acts as:

- Dispatch state engine
- Operational snapshot
- AI retrieval source
- Graph synchronization source
- Dashboard source

Core Principle

Events = History

State = Current Truth

Version:
1.0
"""

import json

from pathlib import Path

from datetime import datetime

STATE_DIR = Path("generated")

STATE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class CurrentStateStore:

    """
    Master state projection store.
    """

    def __init__(self):

        self.jobs = {}

        self.customers = {}

        self.shipments = {}

        self.vehicles = {}

        self.crews = {}

        self.locations = {}

        self.equipment = {}

    # ==================================================
    # JOBS
    # ==================================================

    def upsert_job(
        self,
        job_id,
        data
    ):

        current = self.jobs.get(
            job_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.jobs[
            job_id
        ] = current

    def get_job(
        self,
        job_id
    ):

        return self.jobs.get(
            job_id
        )

    # ==================================================
    # CUSTOMERS
    # ==================================================

    def upsert_customer(
        self,
        customer_id,
        data
    ):

        current = self.customers.get(
            customer_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.customers[
            customer_id
        ] = current

    # ==================================================
    # SHIPMENTS
    # ==================================================

    def upsert_shipment(
        self,
        shipment_id,
        data
    ):

        current = self.shipments.get(
            shipment_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.shipments[
            shipment_id
        ] = current

    # ==================================================
    # VEHICLES
    # ==================================================

    def upsert_vehicle(
        self,
        vehicle_id,
        data
    ):

        current = self.vehicles.get(
            vehicle_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.vehicles[
            vehicle_id
        ] = current

    # ==================================================
    # CREWS
    # ==================================================

    def upsert_crew(
        self,
        crew_id,
        data
    ):

        current = self.crews.get(
            crew_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.crews[
            crew_id
        ] = current

    # ==================================================
    # EQUIPMENT
    # ==================================================

    def upsert_equipment(
        self,
        equipment_id,
        data
    ):

        current = self.equipment.get(
            equipment_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.equipment[
            equipment_id
        ] = current

    # ==================================================
    # LOCATIONS
    # ==================================================

    def upsert_location(
        self,
        location_id,
        data
    ):

        current = self.locations.get(
            location_id,
            {}
        )

        current.update(data)

        current[
            "lastUpdated"
        ] = datetime.utcnow().isoformat()

        self.locations[
            location_id
        ] = current

    # ==================================================
    # EVENT APPLICATION
    # ==================================================

    def apply_event(
        self,
        event
    ):

        event_type = event.get(
            "eventType"
        )

        handlers = {

            "JOB_CREATED":
            self.handle_job_created,

            "ESTIMATE_GENERATED":
            self.handle_estimate_generated,

            "VEHICLE_ASSIGNED":
            self.handle_vehicle_assigned,

            "CREW_ASSIGNED":
            self.handle_crew_assigned,

            "PICKUP_STARTED":
            self.handle_pickup_started,

            "DELIVERY_COMPLETED":
            self.handle_delivery_completed
        }

        handler = handlers.get(
            event_type
        )

        if handler:

            handler(event)

    # ==================================================
    # EVENT HANDLERS
    # ==================================================

    def handle_job_created(
        self,
        event
    ):

        self.upsert_job(

            event["jobId"],

            {
                "status":
                "CREATED",

                "customerId":
                event.get(
                    "customerId"
                ),

                "serviceType":
                event.get(
                    "serviceType"
                ),

                "createdAt":
                event.get(
                    "eventTimestamp"
                )
            }
        )

    def handle_estimate_generated(
        self,
        event
    ):

        self.upsert_job(

            event["jobId"],

            {
                "estimateId":
                event.get(
                    "estimateId"
                ),

                "estimatedPrice":
                event.get(
                    "estimatedPrice"
                )
            }
        )

    def handle_vehicle_assigned(
        self,
        event
    ):

        job = self.jobs.get(
            event["jobId"],
            {}
        )

        vehicle_ids = job.get(
            "vehicleIds",
            []
        )

        vehicle_ids.append(
            event[
                "vehicleId"
            ]
        )

        self.upsert_job(

            event["jobId"],

            {
                "vehicleIds":
                list(
                    set(vehicle_ids)
                ),

                "status":
                "VEHICLE_ASSIGNED"
            }
        )

    def handle_crew_assigned(
        self,
        event
    ):

        job = self.jobs.get(
            event["jobId"],
            {}
        )

        crew_ids = job.get(
            "crewIds",
            []
        )

        crew_ids.append(
            event[
                "crewId"
            ]
        )

        self.upsert_job(

            event["jobId"],

            {
                "crewIds":
                list(
                    set(crew_ids)
                ),

                "status":
                "CREW_ASSIGNED"
            }
        )

    def handle_pickup_started(
        self,
        event
    ):

        self.upsert_job(

            event["jobId"],

            {
                "status":
                "IN_TRANSIT",

                "pickupStarted":
                event.get(
                    "eventTimestamp"
                )
            }
        )

    def handle_delivery_completed(
        self,
        event
    ):

        self.upsert_job(

            event["jobId"],

            {
                "status":
                "COMPLETED",

                "completedAt":
                event.get(
                    "eventTimestamp"
                )
            }
        )

    # ==================================================
    # EXPORTS
    # ==================================================

    def save_state(self):

        exports = {

            "job-state.json":
            self.jobs,

            "customer-state.json":
            self.customers,

            "shipment-state.json":
            self.shipments,

            "vehicle-state.json":
            self.vehicles,

            "crew-state.json":
            self.crews,

            "equipment-state.json":
            self.equipment,

            "location-state.json":
            self.locations
        }

        for filename, data in exports.items():

            with open(

                STATE_DIR / filename,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    data,

                    f,

                    indent=2,

                    ensure_ascii=False

                )

    # ==================================================
    # SNAPSHOT
    # ==================================================

    def system_snapshot(self):

        return {

            "jobs":
            len(self.jobs),

            "customers":
            len(self.customers),

            "shipments":
            len(self.shipments),

            "vehicles":
            len(self.vehicles),

            "crews":
            len(self.crews),

            "equipment":
            len(self.equipment),

            "locations":
            len(self.locations),

            "generated":
            datetime.utcnow().isoformat()
        }


STATE_STORE = CurrentStateStore()
