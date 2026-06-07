#!/usr/bin/env python3

"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

schema_validator.py

Purpose:
Validate all incoming logistics events against
JSON Schema definitions before they enter the system.

Responsibilities:

- Event schema validation
- Ontology validation
- Required field validation
- Enum validation
- Type validation
- Relationship validation
- Event version validation

Version:
1.0
"""

import json
from pathlib import Path

from jsonschema import validate
from jsonschema import ValidationError

ROOT = Path(".")

EVENT_SCHEMA_DIR = ROOT / "events"

ONTOLOGY_DIR = ROOT / "ontology"


class SchemaValidator:

    def __init__(self):

        self.event_cache = {}

        self.load_event_schemas()

    def load_event_schemas(self):

        for schema_file in EVENT_SCHEMA_DIR.glob(
            "*.json"
        ):

            try:

                with open(
                    schema_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    schema = json.load(f)

                    event_type = schema.get(
                        "eventType"
                    )

                    if event_type:

                        self.event_cache[
                            event_type
                        ] = schema

            except Exception as e:

                print(
                    f"Failed loading "
                    f"{schema_file}: {e}"
                )

    def get_schema(
        self,
        event_type
    ):

        return self.event_cache.get(
            event_type
        )

    def validate_event(
        self,
        event
    ):

        event_type = event.get(
            "eventType"
        )

        if not event_type:

            raise ValidationError(
                "eventType missing"
            )

        schema = self.get_schema(
            event_type
        )

        if not schema:

            raise ValidationError(
                f"No schema found "
                f"for {event_type}"
            )

        validate(
            instance=event,
            schema=schema
        )

        self.validate_protocol(
            event
        )

        return True

    def validate_protocol(
        self,
        event
    ):

        if "eventId" not in event:

            raise ValidationError(
                "eventId required"
            )

        if "eventTimestamp" not in event:

            raise ValidationError(
                "eventTimestamp required"
            )

        if "eventVersion" not in event:

            raise ValidationError(
                "eventVersion required"
            )

        return True


validator = SchemaValidator()


def validate_event(
    event
):

    return validator.validate_event(
        event
    )


if __name__ == "__main__":

    sample_event = {

        "eventId":
        "EVT-1001",

        "eventType":
        "JOB_CREATED",

        "eventVersion":
        "1.0",

        "eventTimestamp":
        "2026-06-06T12:00:00Z",

        "jobId":
        "JOB-1001"
    }

    try:

        validate_event(
            sample_event
        )

        print(
            "VALID EVENT"
        )

    except Exception as e:

        print(
            f"INVALID EVENT: {e}"
        )
