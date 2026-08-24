#!/usr/bin/env python3
"""Canonical validation for logistics event envelopes and event-specific schemas."""

import json
from pathlib import Path
from urllib.parse import urljoin

from jsonschema import Draft202012Validator, ValidationError, RefResolver

ROOT = Path(__file__).resolve().parents[1]
EVENT_SCHEMA_DIR = ROOT / "events"


class SchemaValidator:
    """Loads event schemas and resolves their local inheritance references."""

    def __init__(self):
        self.event_cache = {}
        self.load_event_schemas()

    @staticmethod
    def _event_type_from_schema(schema, schema_file):
        # Event-specific schemas currently express the identifier as
        # properties.eventType.const inside an allOf branch.
        direct = schema.get("eventType")
        if isinstance(direct, str):
            return direct

        for branch in schema.get("allOf", []):
            const = branch.get("properties", {}).get("eventType", {}).get("const")
            if isinstance(const, str):
                return const

        # Fallback for a conventional <event-type>.schema.json filename.
        stem = schema_file.stem
        if stem.endswith(".schema"):
            stem = stem[:-7]
        return stem.replace("-", "_").upper() if stem else None

    def load_event_schemas(self):
        self.event_cache.clear()
        for schema_file in EVENT_SCHEMA_DIR.glob("*.schema.json"):
            try:
                with schema_file.open("r", encoding="utf-8") as handle:
                    schema = json.load(handle)
                event_type = self._event_type_from_schema(schema, schema_file)
                if event_type:
                    self.event_cache[event_type] = (schema, schema_file)
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Failed loading {schema_file}: {exc}") from exc

    def get_schema(self, event_type):
        item = self.event_cache.get(event_type)
        return item[0] if item else None

    def validate_event(self, event):
        event_type = event.get("eventType")
        if not event_type:
            raise ValidationError("eventType missing")

        item = self.event_cache.get(event_type)
        if not item:
            raise ValidationError(f"No event-specific schema found for {event_type}")

        schema, schema_file = item
        resolver = RefResolver(
            base_uri=schema_file.resolve().as_uri().replace(schema_file.name, ""),
            referrer=schema,
        )
        Draft202012Validator(schema, resolver=resolver).validate(event)
        self.validate_protocol(event)
        return True

    def validate_protocol(self, event):
        required = (
            "eventId", "eventType", "eventVersion", "eventTimestamp",
            "eventSource", "entityType", "entityId", "correlationId", "stateTransition"
        )
        missing = [field for field in required if field not in event]
        if missing:
            raise ValidationError(f"Required protocol fields missing: {', '.join(missing)}")
        return True


validator = SchemaValidator()


def validate_event(event):
    return validator.validate_event(event)


if __name__ == "__main__":
    sample_event = {
        "eventId": "550e8400-e29b-41d4-a716-446655440000",
        "eventType": "JOB_CREATED",
        "eventVersion": "1.0.0",
        "eventTimestamp": "2026-08-24T09:00:00Z",
        "eventSource": "dispatch",
        "entityType": "job",
        "entityId": "JOB-1001",
        "correlationId": "CORR-1001",
        "stateTransition": {
            "previousState": "REQUEST_RECEIVED",
            "newState": "JOB_CREATED"
        },
        "payload": {
            "jobNumber": "JOB-1001",
            "customer": {},
            "service": {},
            "origin": {},
            "destination": {},
            "requestedDate": "2026-08-24"
        }
    }
    validate_event(sample_event)
    print("VALID EVENT")
