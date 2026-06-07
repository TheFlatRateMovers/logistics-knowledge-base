#!/usr/bin/env python3

"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

event_router.py

Purpose:

Central routing engine
for all logistics events.

Pipeline:

Event
 ↓
Validation
 ↓
Projection
 ↓
Graph Sync
 ↓
Future AI Agents

Version:
1.0
"""

import json

from pathlib import Path

from schema_validator import (
    validate_event
)

ROOT = Path(".")

EVENT_QUEUE = (
    ROOT /
    "event-stream"
)

PROCESSED = (
    ROOT /
    "processed-events"
)

PROCESSED.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================================
# HANDLER REGISTRY
# =====================================================

class EventRouter:

    def __init__(self):

        self.handlers = {

            "JOB_CREATED":
            self.job_created,

            "ESTIMATE_GENERATED":
            self.estimate_generated,

            "VEHICLE_ASSIGNED":
            self.vehicle_assigned,

            "CREW_ASSIGNED":
            self.crew_assigned,

            "PICKUP_STARTED":
            self.pickup_started,

            "IN_TRANSIT":
            self.in_transit,

            "DELIVERY_COMPLETED":
            self.delivery_completed
        }

    # ==========================================
    # ROUTING
    # ==========================================

    def route(
        self,
        event
    ):

        validate_event(
            event
        )

        event_type = event[
            "eventType"
        ]

        handler = self.handlers.get(
            event_type
        )

        if not handler:

            raise Exception(
                f"No handler for "
                f"{event_type}"
            )

        return handler(
            event
        )

    # ==========================================
    # EVENT HANDLERS
    # ==========================================

    def job_created(
        self,
        event
    ):

        print(
            f"[JOB CREATED] "
            f"{event['jobId']}"
        )

        return {

            "status":
            "processed",

            "eventType":
            "JOB_CREATED"
        }

    def estimate_generated(
        self,
        event
    ):

        print(
            f"[ESTIMATE]"
        )

        return {

            "status":
            "processed",

            "eventType":
            "ESTIMATE_GENERATED"
        }

    def vehicle_assigned(
        self,
        event
    ):

        print(
            f"[VEHICLE]"
        )

        return {

            "status":
            "processed",

            "eventType":
            "VEHICLE_ASSIGNED"
        }

    def crew_assigned(
        self,
        event
    ):

        print(
            f"[CREW]"
        )

        return {

            "status":
            "processed",

            "eventType":
            "CREW_ASSIGNED"
        }

    def pickup_started(
        self,
        event
    ):

        print(
            f"[PICKUP]"
        )

        return {

            "status":
            "processed",

            "eventType":
            "PICKUP_STARTED"
        }

    def in_transit(
        self,
        event
    ):

        print(
            f"[TRANSIT]"
        )

        return {

            "status":
            "processed",

            "eventType":
            "IN_TRANSIT"
        }

    def delivery_completed(
        self,
        event
    ):

        print(
            f"[DELIVERED]"
        )

        return {

            "status":
            "processed",

            "eventType":
            "DELIVERY_COMPLETED"
        }


# =====================================================
# FILE INGESTION
# =====================================================

def process_file(
    filepath,
    router
):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        event = json.load(f)

    result = router.route(
        event
    )

    destination = (
        PROCESSED /
        filepath.name
    )

    filepath.rename(
        destination
    )

    return result


# =====================================================
# EVENT STREAM LOOP
# =====================================================

def run_event_stream():

    router = EventRouter()

    files = list(

        EVENT_QUEUE.glob(
            "*.json"
        )
    )

    for file in files:

        try:

            process_file(
                file,
                router
            )

        except Exception as e:

            print(

                f"ERROR "
                f"{file.name}: {e}"

            )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    run_event_stream()
