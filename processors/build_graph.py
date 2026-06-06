"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

Graph Builder v1.0

Purpose:
Build a unified logistics knowledge graph from:

- ontology
- entities
- events
- datasets
- knowledge-graphs
- supergraphs

Outputs:

/generated/graph-nodes.json
/generated/graph-edges.json
/generated/rdf-triples.json
/generated/neo4j-import.json
/generated/retrieval-index.json

Compatible With:

- GraphRAG
- Neo4j
- RDF
- JSON-LD
- Semantic Retrieval
- AI Agents
"""

import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(".")

OUTPUT_DIR = ROOT / "generated"

OUTPUT_DIR.mkdir(exist_ok=True)

SUPPORTED_EXTENSIONS = [".json"]


# =====================================================
# GRAPH STORAGE
# =====================================================

graph_nodes = {}
graph_edges = []
rdf_triples = []

retrieval_index = {
    "generatedAt": datetime.utcnow().isoformat(),
    "entities": [],
    "services": [],
    "ports": [],
    "corridors": [],
    "datasets": [],
    "knowledgeResources": []
}


# =====================================================
# FILE DISCOVERY
# =====================================================

def discover_json_files():

    discovered = []

    target_folders = [
        "ontology",
        "entities",
        "events",
        "datasets",
        "knowledge-graphs",
        "supergraphs",
        "counties",
        "regional-entities",
        "service-demand"
    ]

    for folder in target_folders:

        path = ROOT / folder

        if not path.exists():
            continue

        for file in path.rglob("*.json"):
            discovered.append(file)

    return discovered


# =====================================================
# LOAD JSON
# =====================================================

def load_json(file_path):

    try:

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:

        print(f"ERROR loading {file_path}")
        print(e)

        return None


# =====================================================
# NODE CREATION
# =====================================================

def create_node(node_id, node_type, properties):

    if node_id not in graph_nodes:

        graph_nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "properties": properties
        }


# =====================================================
# EDGE CREATION
# =====================================================

def create_edge(source, relationship, target):

    edge = {
        "source": source,
        "relationship": relationship,
        "target": target
    }

    graph_edges.append(edge)

    rdf_triples.append({
        "subject": source,
        "predicate": relationship,
        "object": target
    })


# =====================================================
# SERVICE PROCESSOR
# =====================================================

def process_services(data):

    services = data.get("services", [])

    for service in services:

        service_id = f"service:{service}"

        create_node(
            service_id,
            "Service",
            {"name": service}
        )

        retrieval_index["services"].append(service)


# =====================================================
# PORT PROCESSOR
# =====================================================

def process_ports(data):

    ports = data.get("ports", [])

    for port in ports:

        if isinstance(port, dict):

            name = port.get("name")

        else:

            name = port

        if not name:
            continue

        port_id = f"port:{name}"

        create_node(
            port_id,
            "Port",
            {"name": name}
        )

        retrieval_index["ports"].append(name)


# =====================================================
# CORRIDOR PROCESSOR
# =====================================================

def process_corridors(data):

    corridors = data.get("corridors", [])

    for corridor in corridors:

        corridor_id = f"corridor:{corridor}"

        create_node(
            corridor_id,
            "Corridor",
            {"name": corridor}
        )

        retrieval_index["corridors"].append(corridor)


# =====================================================
# COUNTY PROCESSOR
# =====================================================

def process_county_file(data):

    county = data.get("county")

    if not county:
        return

    county_id = f"county:{county}"

    create_node(
        county_id,
        "County",
        {"name": county}
    )

    for city in data.get("cities", []):

        city_id = f"city:{city}"

        create_node(
            city_id,
            "City",
            {"name": city}
        )

        create_edge(
            city_id,
            "LOCATED_IN_COUNTY",
            county_id
        )

    for zip_code in data.get("zipCodes", []):

        zip_id = f"zip:{zip_code}"

        create_node(
            zip_id,
            "ZipCode",
            {"zip": zip_code}
        )

        create_edge(
            zip_id,
            "LOCATED_IN_COUNTY",
            county_id
        )

    for corridor in data.get("corridors", []):

        corridor_id = f"corridor:{corridor}"

        create_node(
            corridor_id,
            "Corridor",
            {"name": corridor}
        )

        create_edge(
            county_id,
            "SERVED_BY",
            corridor_id
        )

    for service in data.get("services", []):

        service_id = f"service:{service}"

        create_node(
            service_id,
            "Service",
            {"name": service}
        )

        create_edge(
            county_id,
            "SUPPORTS",
            service_id
        )


# =====================================================
# ZIP GRAPH PROCESSOR
# =====================================================

def process_zip_graph(data):

    nodes = data.get("nodes", [])

    for node in nodes:

        node_id = node.get("id")

        if not node_id:
            continue

        create_node(
            node_id,
            node.get("type", "Entity"),
            node
        )

    edges = data.get("edges", [])

    for edge in edges:

        create_edge(
            edge["source"],
            edge["relationship"],
            edge["target"]
        )


# =====================================================
# GENERIC ENTITY EXTRACTION
# =====================================================

def process_generic(data):

    process_services(data)
    process_ports(data)
    process_corridors(data)


# =====================================================
# FILE ROUTING
# =====================================================

def process_file(file_path):

    data = load_json(file_path)

    if not data:
        return

    file_name = file_path.name

    retrieval_index["datasets"].append(str(file_path))

    if "county" in data:
        process_county_file(data)

    elif "nodes" in data and "edges" in data:
        process_zip_graph(data)

    else:
        process_generic(data)


# =====================================================
# EXPORTS
# =====================================================

def export_graph():

    with open(
        OUTPUT_DIR / "graph-nodes.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            list(graph_nodes.values()),
            f,
            indent=2
        )

    with open(
        OUTPUT_DIR / "graph-edges.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            graph_edges,
            f,
            indent=2
        )

    with open(
        OUTPUT_DIR / "rdf-triples.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rdf_triples,
            f,
            indent=2
        )

    with open(
        OUTPUT_DIR / "neo4j-import.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "nodes": list(graph_nodes.values()),
                "relationships": graph_edges
            },
            f,
            indent=2
        )

    with open(
        OUTPUT_DIR / "retrieval-index.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            retrieval_index,
            f,
            indent=2
        )


# =====================================================
# MAIN
# =====================================================

def build_graph():

    files = discover_json_files()

    print(f"FILES DISCOVERED: {len(files)}")

    for file in files:

        process_file(file)

    export_graph()

    print(
        f"NODES: {len(graph_nodes)} | "
        f"EDGES: {len(graph_edges)}"
    )


if __name__ == "__main__":

    build_graph()
