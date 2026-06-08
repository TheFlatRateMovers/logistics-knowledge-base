"""
State Reducer
Logistics Event & Graph Protocol v1.0

Repository Path:
/processors/state-reducer.py

Purpose:

Convert event history
into current operational state.

Core Principle:

Events = History

State = Reality

Supported Entities:

- Jobs
- Customers
- Vehicles
- Crews
- Shipments
- Equipment
- Locations

"""

from typing import Dict
from typing import List


class StateReducer:

    def __init__(self):

        self.state = {

            "jobs": {},

            "customers": {},

            "vehicles": {},

            "crews": {},

            "shipments": {}
        }

    def apply_event(

        self,

        event: Dict

    ):

        event_type = event.get(

            "event_type"

        )

        if event_type == "JOB_CREATED":

            self._job_created(

                event

            )

        elif event_type == "ESTIMATE_GENERATED":

            self._estimate_generated(

                event

            )

        elif event_type == "VEHICLE_ASSIGNED":

            self._vehicle_assigned(

                event

            )

        elif event_type == "CREW_ASSIGNED":

            self._crew_assigned(

                event

            )

        elif event_type == "PICKUP_STARTED":

            self._pickup_started(

                event

            )

        elif event_type == "DELIVERY_COMPLETED":

            self._delivery_completed(

                event

            )

    def _job_created(

        self,

        event

    ):

        self.state["jobs"][

            event["job_id"]

        ] = {

            "status": "created",

            "service_type":

            event["payload"].get(

                "service_type"

            ),

            "vehicle": None,

            "crew": None
        }

    def _estimate_generated(

        self,

        event

    ):

        job = self.state["jobs"].get(

            event["job_id"]

        )

        if job:

            job["estimate"] = (

                event["payload"]

                .get("estimate")

            )

    def _vehicle_assigned(

        self,

        event

    ):

        job = self.state["jobs"].get(

            event["job_id"]

        )

        if job:

            job["vehicle"] = (

                event["payload"]

                .get("vehicle_id")

            )

    def _crew_assigned(

        self,

        event

    ):

        job = self.state["jobs"].get(

            event["job_id"]

        )

        if job:

            job["crew"] = (

                event["payload"]

                .get("crew")

            )

    def _pickup_started(

        self,

        event

    ):

        job = self.state["jobs"].get(

            event["job_id"]

        )

        if job:

            job["status"] = (

                "pickup_started"

            )

    def _delivery_completed(

        self,

        event

    ):

        job = self.state["jobs"].get(

            event["job_id"]

        )

        if job:

            job["status"] = (

                "completed"

            )

    def build_state(

        self,

        events: List[Dict]

    ):

        for event in events:

            self.apply_event(

                event

            )

        return self.state


if __name__ == "__main__":

    reducer = StateReducer()

    print(

        "State Reducer Ready"

    )
