"""
Event Store
Logistics Event & Graph Protocol v1.0

Repository Path:
/processors/event-store.py

Purpose:
Immutable event storage layer.

Responsibilities:

- Persist all logistics events
- Maintain chronological event history
- Support event replay
- Support state reconstruction
- Support AI reasoning pipelines
- Support GraphRAG ingestion
- Support Neo4j projection

Architecture:

EVENT
  ↓
EVENT STORE
  ↓
STATE REDUCER
  ↓
GRAPH PROJECTION
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class EventStore:

    def __init__(
        self,
        storage_directory: str = "event_store"
    ):

        self.storage_directory = Path(
            storage_directory
        )

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def append_event(
        self,
        event: Dict
    ) -> Dict:

        if "event_id" not in event:

            event["event_id"] = str(
                uuid.uuid4()
            )

        if "timestamp" not in event:

            event["timestamp"] = (
                datetime.utcnow()
                .isoformat()
            )

        date_partition = (
            datetime.utcnow()
            .strftime("%Y-%m-%d")
        )

        partition_file = (
            self.storage_directory /
            f"{date_partition}.jsonl"
        )

        with open(
            partition_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(event)
            )

            file.write("\n")

        return event

    def read_partition(
        self,
        date_partition: str
    ) -> List[Dict]:

        file_path = (
            self.storage_directory /
            f"{date_partition}.jsonl"
        )

        if not file_path.exists():

            return []

        events = []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                events.append(
                    json.loads(line)
                )

        return events

    def replay_events(
        self
    ) -> List[Dict]:

        events = []

        for file_path in sorted(

            self.storage_directory.glob(
                "*.jsonl"
            )

        ):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:

                    events.append(

                        json.loads(line)

                    )

        return events

    def get_event(
        self,
        event_id: str
    ) -> Optional[Dict]:

        for event in self.replay_events():

            if event.get(
                "event_id"
            ) == event_id:

                return event

        return None

    def get_events_by_type(
        self,
        event_type: str
    ) -> List[Dict]:

        results = []

        for event in self.replay_events():

            if event.get(
                "event_type"
            ) == event_type:

                results.append(event)

        return results

    def get_events_by_job(
        self,
        job_id: str
    ) -> List[Dict]:

        results = []

        for event in self.replay_events():

            if event.get(
                "job_id"
            ) == job_id:

                results.append(event)

        return results


if __name__ == "__main__":

    store = EventStore()

    sample_event = {

        "event_type":
        "JOB_CREATED",

        "job_id":
        "JOB-1001",

        "payload": {

            "service_type":
            "Data Center Relocation"
        }
    }

    store.append_event(
        sample_event
    )

    print(
        "Event stored successfully."
    )
