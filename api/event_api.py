"""
Event API
Logistics Event & Graph Protocol v1.0

Repository Path:
/api/event_api.py

Purpose:
External ingestion layer for logistics events.

Responsibilities:
- Receive events
- Validate events
- Store events
- Trigger state projection
- Trigger graph projection
- Trigger AI workflows

Architecture:

External Systems
      ↓
Event API
      ↓
Schema Validation
      ↓
Event Store
      ↓
State Reducer
      ↓
Graph Projection
      ↓
AI Agents
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Any
import uuid

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

SUPPORTED_EVENTS = [

    "JOB_CREATED",

    "ESTIMATE_GENERATED",

    "CREW_ASSIGNED",

    "VEHICLE_ASSIGNED",

    "PICKUP_STARTED",

    "IN_TRANSIT",

    "DELIVERY_COMPLETED",

    "DELAY_REPORTED",

    "DAMAGE_REPORTED",

    "PAYMENT_RECEIVED"
]


class EventValidator:

    @staticmethod
    def validate(event: Dict) -> Dict:

        required_fields = [

            "event_type",

            "job_id",

            "payload"
        ]

        missing = [

            field

            for field in required_fields

            if field not in event
        ]

        if missing:

            return {

                "valid": False,

                "errors": missing
            }

        if event["event_type"] not in SUPPORTED_EVENTS:

            return {

                "valid": False,

                "errors": [

                    "unsupported_event_type"
                ]
            }

        return {

            "valid": True,

            "errors": []
        }


class EventAPI:

    @staticmethod
    def enrich_event(event):

        event["event_id"] = str(

            uuid.uuid4()

        )

        event["timestamp"] = (

            datetime.utcnow()

            .isoformat()

        )

        event["protocol"] = (

            "Logistics Event & Graph Protocol"

        )

        event["version"] = "1.0.0"

        return event


@app.route(

    "/events",

    methods=["POST"]

)
def create_event():

    event = request.get_json()

    validation = (

        EventValidator.validate(

            event

        )

    )

    if not validation["valid"]:

        return jsonify({

            "status": "error",

            "errors":

            validation["errors"]

        }), 400

    event = (

        EventAPI.enrich_event(

            event

        )

    )

    return jsonify({

        "status": "accepted",

        "event": event

    }), 202


@app.route(

    "/events/health",

    methods=["GET"]

)
def health():

    return jsonify({

        "status": "healthy",

        "service": "event_api",

        "version": "1.0.0"

    })


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8000,

        debug=True

    )
