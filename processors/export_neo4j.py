"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

Neo4j Export Engine v1.0

Purpose:
Convert protocol graph assets into:

- Neo4j node CSV
- Neo4j relationship CSV
- Cypher import script
- Graph statistics
- GraphRAG exports

Inputs:

generated/
    graph-nodes.json
    graph-edges.json

Outputs:

exports/neo4j/
    nodes.csv
    relationships.csv
    import.cypher
    graph-statistics.json
    graphrag-export.json

Compatible With:

- Neo4j Community
- Neo4j Enterprise
- Memgraph
- FalkorDB
- GraphRAG
- Vector Knowledge Systems
"""

import csv
import json
from pathlib import Path
from collections import Counter

ROOT = Path(".")

GENERATED_DIR = ROOT / "generated"

EXPORT_DIR = ROOT / "exports" / "neo4j"

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOADERS
# ============================================================

def load_json(filename):

    file_path = GENERATED_DIR / filename

    if not file_path.exists():

        raise FileNotFoundError(
            f"Missing required file: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ============================================================
# SOURCE DATA
# ============================================================

NODES = load_json("graph-nodes.json")

EDGES = load_json("graph-edges.json")


# ============================================================
# PROPERTY FLATTENER
# ============================================================

def flatten_properties(properties):

    flattened = {}

    if not isinstance(properties, dict):
        return flattened

    for key, value in properties.items():

        if isinstance(value, list):

            flattened[key] = "|".join(
                str(v) for v in value
            )

        elif isinstance(value, dict):

            flattened[key] = json.dumps(value)

        else:

            flattened[key] = value

    return flattened


# ============================================================
# COLLECT PROPERTY FIELDS
# ============================================================

def collect_property_fields():

    fields = set()

    for node in NODES:

        props = node.get(
            "properties",
            {}
        )

        fields.update(
            flatten_properties(props).keys()
        )

    return sorted(fields)


# ============================================================
# EXPORT NODE CSV
# ============================================================

def export_nodes_csv():

    property_fields = collect_property_fields()

    csv_file = EXPORT_DIR / "nodes.csv"

    headers = [
        "id:ID",
        ":LABEL"
    ]

    headers.extend(property_fields)

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=headers
        )

        writer.writeheader()

        for node in NODES:

            row = {
                "id:ID": node.get("id"),
                ":LABEL": node.get("type", "Entity")
            }

            row.update(
                flatten_properties(
                    node.get(
                        "properties",
                        {}
                    )
                )
            )

            writer.writerow(row)

    print("nodes.csv exported")


# ============================================================
# EXPORT RELATIONSHIPS CSV
# ============================================================

def export_relationships_csv():

    csv_file = (
        EXPORT_DIR /
        "relationships.csv"
    )

    headers = [
        ":START_ID",
        ":END_ID",
        ":TYPE"
    ]

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=headers
        )

        writer.writeheader()

        for edge in EDGES:

            writer.writerow({

                ":START_ID":
                edge["source"],

                ":END_ID":
                edge["target"],

                ":TYPE":
                edge["relationship"]
            })

    print("relationships.csv exported")


# ============================================================
# CYPHER IMPORT SCRIPT
# ============================================================

def export_cypher():

    cypher = """
CREATE CONSTRAINT node_id_unique IF NOT EXISTS
FOR (n:Entity)
REQUIRE n.id IS UNIQUE;

LOAD CSV WITH HEADERS
FROM 'file:///nodes.csv'
AS row

MERGE (n:Entity {id: row.`id:ID`})

SET n += row;

LOAD CSV WITH HEADERS
FROM 'file:///relationships.csv'
AS row

MATCH (s {id: row.`:START_ID`})
MATCH (t {id: row.`:END_ID`})

CALL apoc.create.relationship(
    s,
    row.`:TYPE`,
    {},
    t
) YIELD rel

RETURN count(rel);
"""

    with open(
        EXPORT_DIR / "import.cypher",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(cypher)

    print("import.cypher exported")


# ============================================================
# GRAPH STATISTICS
# ============================================================

def export_statistics():

    node_types = Counter()

    relationship_types = Counter()

    for node in NODES:

        node_types[
            node.get(
                "type",
                "Unknown"
            )
        ] += 1

    for edge in EDGES:

        relationship_types[
            edge.get(
                "relationship",
                "UNKNOWN"
            )
        ] += 1

    stats = {

        "totalNodes":
        len(NODES),

        "totalRelationships":
        len(EDGES),

        "nodeTypes":
        dict(node_types),

        "relationshipTypes":
        dict(relationship_types)
    }

    with open(
        EXPORT_DIR /
        "graph-statistics.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            stats,
            f,
            indent=2
        )

    print(
        "graph-statistics.json exported"
    )


# ============================================================
# GRAPHRAG EXPORT
# ============================================================

def export_graphrag():

    records = []

    for node in NODES:

        node_id = node.get("id")

        connected_edges = []

        for edge in EDGES:

            if (
                edge["source"] == node_id
                or
                edge["target"] == node_id
            ):

                connected_edges.append(edge)

        records.append({

            "entityId":
            node_id,

            "entityType":
            node.get("type"),

            "properties":
            node.get(
                "properties",
                {}
            ),

            "relationships":
            connected_edges
        })

    with open(
        EXPORT_DIR /
        "graphrag-export.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            records,
            f,
            indent=2
        )

    print(
        "graphrag-export.json exported"
    )


# ============================================================
# VALIDATION
# ============================================================

def validate_graph():

    node_ids = {

        node["id"]

        for node in NODES
    }

    missing = []

    for edge in EDGES:

        if edge["source"] not in node_ids:

            missing.append(
                edge["source"]
            )

        if edge["target"] not in node_ids:

            missing.append(
                edge["target"]
            )

    if missing:

        raise ValueError(
            f"Missing node references: "
            f"{sorted(set(missing))}"
        )

    print(
        "Graph validation passed"
    )


# ============================================================
# MAIN
# ============================================================

def export_neo4j():

    print(
        "Starting Neo4j export..."
    )

    validate_graph()

    export_nodes_csv()

    export_relationships_csv()

    export_cypher()

    export_statistics()

    export_graphrag()

    print(
        "Neo4j export complete"
    )


if __name__ == "__main__":

    export_neo4j()
