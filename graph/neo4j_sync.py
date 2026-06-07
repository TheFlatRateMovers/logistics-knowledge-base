#!/usr/bin/env python3

"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

neo4j_sync.py

Purpose:
Synchronize projected logistics state
into Neo4j knowledge graphs.

Supports:

- Jobs
- Customers
- Shipments
- Vehicles
- Crews
- Equipment
- Locations

Graph Model:

(Job)-[:ASSIGNED_TO]->(Vehicle)

(Job)-[:HANDLED_BY]->(Crew)

(Job)-[:ORIGIN]->(Location)

(Job)-[:DESTINATION]->(Location)

(Customer)-[:OWNS]->(Shipment)

(Shipment)-[:USES]->(Equipment)

Version:
1.0
"""

import json

from pathlib import Path

from neo4j import GraphDatabase

# =====================================================
# CONFIGURATION
# =====================================================

NEO4J_URI = "bolt://localhost:7687"

NEO4J_USER = "neo4j"

NEO4J_PASSWORD = "password"

GENERATED_DIR = Path(
    "generated"
)

# =====================================================
# DRIVER
# =====================================================

class Neo4jSync:

    def __init__(

        self,

        uri,

        user,

        password

    ):

        self.driver = (

            GraphDatabase.driver(

                uri,

                auth=(

                    user,

                    password

                )

            )

        )

    def close(self):

        self.driver.close()

# =====================================================
# LOAD JSON
# =====================================================

    def load_json(

        self,

        filename

    ):

        file_path = (

            GENERATED_DIR /

            filename

        )

        if not file_path.exists():

            return {}

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

# =====================================================
# CONSTRAINTS
# =====================================================

    def create_constraints(self):

        statements = [

            """
            CREATE CONSTRAINT job_id
            IF NOT EXISTS
            FOR (j:Job)
            REQUIRE j.jobId IS UNIQUE
            """,

            """
            CREATE CONSTRAINT shipment_id
            IF NOT EXISTS
            FOR (s:Shipment)
            REQUIRE s.shipmentId IS UNIQUE
            """,

            """
            CREATE CONSTRAINT customer_id
            IF NOT EXISTS
            FOR (c:Customer)
            REQUIRE c.customerId IS UNIQUE
            """,

            """
            CREATE CONSTRAINT vehicle_id
            IF NOT EXISTS
            FOR (v:Vehicle)
            REQUIRE v.vehicleId IS UNIQUE
            """,

            """
            CREATE CONSTRAINT crew_id
            IF NOT EXISTS
            FOR (c:Crew)
            REQUIRE c.crewId IS UNIQUE
            """,

            """
            CREATE CONSTRAINT equipment_id
            IF NOT EXISTS
            FOR (e:Equipment)
            REQUIRE e.equipmentId IS UNIQUE
            """
        ]

        with self.driver.session() as session:

            for stmt in statements:

                session.run(stmt)

# =====================================================
# JOBS
# =====================================================

    def sync_jobs(self):

        jobs = self.load_json(

            "job-state.json"

        )

        with self.driver.session() as session:

            for job_id, job in jobs.items():

                session.run(

                    """
                    MERGE (j:Job {
                        jobId:$jobId
                    })

                    SET
                        j.status=$status,
                        j.createdAt=$createdAt
                    """,

                    {

                        "jobId":
                        job_id,

                        "status":
                        job.get("status"),

                        "createdAt":
                        job.get("createdAt")

                    }

                )

# =====================================================
# VEHICLES
# =====================================================

    def sync_vehicles(self):

        vehicles = self.load_json(

            "vehicle-state.json"

        )

        with self.driver.session() as session:

            for vehicle_id, vehicle in (

                vehicles.items()

            ):

                session.run(

                    """
                    MERGE (v:Vehicle {
                        vehicleId:$vehicleId
                    })

                    SET
                        v.status=$status
                    """,

                    {

                        "vehicleId":
                        vehicle_id,

                        "status":
                        vehicle.get("status")

                    }

                )

# =====================================================
# CREWS
# =====================================================

    def sync_crews(self):

        crews = self.load_json(

            "crew-state.json"

        )

        with self.driver.session() as session:

            for crew_id, crew in (

                crews.items()

            ):

                session.run(

                    """
                    MERGE (c:Crew {
                        crewId:$crewId
                    })

                    SET
                        c.status=$status
                    """,

                    {

                        "crewId":
                        crew_id,

                        "status":
                        crew.get("status")

                    }

                )

# =====================================================
# JOB → VEHICLE
# =====================================================

    def sync_vehicle_links(self):

        jobs = self.load_json(

            "job-state.json"

        )

        with self.driver.session() as session:

            for job_id, job in jobs.items():

                for vehicle_id in (

                    job.get(

                        "vehicleIds",

                        []

                    )

                ):

                    session.run(

                        """
                        MATCH (j:Job {
                            jobId:$jobId
                        })

                        MATCH (v:Vehicle {
                            vehicleId:$vehicleId
                        })

                        MERGE
                        (j)-[:ASSIGNED_TO]->(v)
                        """,

                        {

                            "jobId":
                            job_id,

                            "vehicleId":
                            vehicle_id

                        }

                    )

# =====================================================
# JOB → CREW
# =====================================================

    def sync_crew_links(self):

        jobs = self.load_json(

            "job-state.json"

        )

        with self.driver.session() as session:

            for job_id, job in jobs.items():

                for crew_id in (

                    job.get(

                        "crewIds",

                        []

                    )

                ):

                    session.run(

                        """
                        MATCH (j:Job {
                            jobId:$jobId
                        })

                        MATCH (c:Crew {
                            crewId:$crewId
                        })

                        MERGE
                        (j)-[:HANDLED_BY]->(c)
                        """,

                        {

                            "jobId":
                            job_id,

                            "crewId":
                            crew_id

                        }

                    )

# =====================================================
# GRAPH METRICS
# =====================================================

    def graph_metrics(self):

        with self.driver.session() as session:

            nodes = session.run(

                """
                MATCH (n)
                RETURN count(n)
                AS total
                """

            ).single()

            edges = session.run(

                """
                MATCH ()-[r]->()
                RETURN count(r)
                AS total
                """

            ).single()

            return {

                "nodes":
                nodes["total"],

                "relationships":
                edges["total"]

            }

# =====================================================
# MASTER SYNC
# =====================================================

    def synchronize(self):

        print(

            "Creating constraints..."

        )

        self.create_constraints()

        print(

            "Syncing jobs..."

        )

        self.sync_jobs()

        print(

            "Syncing vehicles..."

        )

        self.sync_vehicles()

        print(

            "Syncing crews..."

        )

        self.sync_crews()

        print(

            "Syncing relationships..."

        )

        self.sync_vehicle_links()

        self.sync_crew_links()

        metrics = (

            self.graph_metrics()

        )

        print(

            f"Nodes: "
            f"{metrics['nodes']}"

        )

        print(

            f"Relationships: "
            f"{metrics['relationships']}"

        )

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    sync = Neo4jSync(

        NEO4J_URI,

        NEO4J_USER,

        NEO4J_PASSWORD

    )

    try:

        sync.synchronize()

    finally:

        sync.close()
