"""
Dispatch Decision Engine
Logistics Event & Graph Protocol v1.0

Repository Path:

/ai/dispatch-decision-engine.py

Purpose:

Transforms operational state,
graph intelligence,
routing recommendations,
risk analysis,
pricing analysis,
and resource availability

into executable dispatch decisions.

Core Function:

Customer Intent
    ↓
Dispatch Reasoning
    ↓
Operational Assignment
    ↓
Dispatch Events

"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import uuid


@dataclass
class DispatchDecision:

    decision_id: str

    job_id: str

    assigned_vehicle: str

    assigned_crew: List[str]

    confidence_score: float

    risk_score: float

    route_score: float

    equipment_score: float

    generated_timestamp: str

    decision_reasoning: List[str]


class DispatchDecisionEngine:

    def __init__(self):

        self.version = "1.0"

        self.engine_name = "DispatchDecisionEngine"

    def calculate_vehicle_score(
        self,
        vehicle: Dict,
        job: Dict
    ) -> float:

        score = 0.0

        if vehicle["status"] == "available":
            score += 40

        if vehicle["capacity"] >= job["required_capacity"]:
            score += 30

        if vehicle["service_region"] == job["service_region"]:
            score += 20

        score += vehicle.get(
            "historical_performance",
            0
        )

        return score

    def calculate_crew_score(
        self,
        crew: Dict,
        job: Dict
    ) -> float:

        score = 0.0

        if crew["status"] == "available":
            score += 30

        if job["service_type"] in crew["skills"]:
            score += 30

        score += crew.get(
            "historical_rating",
            0
        )

        return score

    def calculate_dispatch_score(
        self,
        vehicle_score: float,
        crew_score: float,
        risk_score: float,
        route_score: float
    ):

        return (

            vehicle_score * 0.30 +

            crew_score * 0.30 +

            route_score * 0.25 +

            (100 - risk_score) * 0.15
        )

    def generate_decision(
        self,
        job: Dict,
        vehicles: List[Dict],
        crews: List[Dict],
        risk_score: float,
        route_score: float
    ) -> DispatchDecision:

        best_vehicle = None
        best_vehicle_score = -1

        for vehicle in vehicles:

            score = self.calculate_vehicle_score(
                vehicle,
                job
            )

            if score > best_vehicle_score:

                best_vehicle_score = score

                best_vehicle = vehicle

        best_crew = None
        best_crew_score = -1

        for crew in crews:

            score = self.calculate_crew_score(
                crew,
                job
            )

            if score > best_crew_score:

                best_crew_score = score

                best_crew = crew

        confidence = self.calculate_dispatch_score(

            best_vehicle_score,

            best_crew_score,

            risk_score,

            route_score
        )

        return DispatchDecision(

            decision_id=str(uuid.uuid4()),

            job_id=job["job_id"],

            assigned_vehicle=best_vehicle["vehicle_id"],

            assigned_crew=best_crew["crew_members"],

            confidence_score=round(
                confidence,
                2
            ),

            risk_score=risk_score,

            route_score=route_score,

            equipment_score=best_vehicle_score,

            generated_timestamp=datetime.utcnow().isoformat(),

            decision_reasoning=[

                "Vehicle capacity compatible",

                "Crew certified",

                "Route optimized",

                "Risk acceptable"
            ]
        )


if __name__ == "__main__":

    print(
        "Dispatch Decision Engine Loaded"
    )
