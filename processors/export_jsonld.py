"""
The Flat Rate Movers LLC
Logistics Event & Graph Protocol

JSON-LD Export Engine v1.0

Purpose:
Transform generated graph assets into:

- JSON-LD
- Schema.org Dataset
- Schema.org DataCatalog
- Knowledge Graph exports
- GraphRAG metadata
- AI Retrieval metadata

Inputs:

generated/
    graph-nodes.json
    graph-edges.json
    rdf-triples.json
    retrieval-index.json

Outputs:

exports/jsonld/
    logistics-datacatalog.jsonld
    logistics-dataset.jsonld
    logistics-knowledge-graph.jsonld
    logistics-services.jsonld
    logistics-corridors.jsonld
    logistics-ports.jsonld
"""

import json

from pathlib import Path
from datetime import datetime

ROOT = Path(".")

GENERATED = ROOT / "generated"

EXPORTS = ROOT / "exports" / "jsonld"

EXPORTS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(file_name):

    file_path = GENERATED / file_name

    if not file_path.exists():
        return []

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

RETRIEVAL = load_json("retrieval-index.json")


# ============================================================
# COMPANY CONSTANTS
# ============================================================

ORGANIZATION = {
    "@type": "Organization",
    "@id": "https://theflatratemovers.com/#organization",
    "name": "The Flat Rate Movers LLC",
    "url": "https://theflatratemovers.com/",
    "telephone": "+1-540-422-2153",
    "email": "ratemovers@gmail.com",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "116 W Piccadilly St Suite 11",
        "addressLocality": "Winchester",
        "addressRegion": "VA",
        "postalCode": "22601",
        "addressCountry": "US"
    }
}


# ============================================================
# SERVICES
# ============================================================

def build_services():

    services = []

    for node in NODES:

        if node.get("type") != "Service":
            continue

        service_name = (
            node.get("properties", {})
            .get("name")
        )

        services.append({

            "@type": "Service",

            "@id":
            f"https://theflatratemovers.com/service/{service_name.lower().replace(' ','-')}",

            "name": service_name,

            "provider": {
                "@id":
                ORGANIZATION["@id"]
            },

            "areaServed": [
                "Virginia",
                "West Virginia",
                "Maryland",
                "Pennsylvania"
            ]
        })

    return services


# ============================================================
# PORTS
# ============================================================

def build_ports():

    ports = []

    for node in NODES:

        if node.get("type") != "Port":
            continue

        name = (
            node.get("properties", {})
            .get("name")
        )

        ports.append({

            "@type": "Place",

            "@id":
            f"https://logistics.theflatratemovers.com/port/{name.lower().replace(' ','-')}",

            "name": name
        })

    return ports


# ============================================================
# CORRIDORS
# ============================================================

def build_corridors():

    corridors = []

    for node in NODES:

        if node.get("type") != "Corridor":
            continue

        name = (
            node.get("properties", {})
            .get("name")
        )

        corridors.append({

            "@type": "DefinedRegion",

            "@id":
            f"https://logistics.theflatratemovers.com/corridor/{name.lower()}",

            "name": name
        })

    return corridors


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

def build_knowledge_graph():

    graph_entities = []

    graph_entities.append(
        ORGANIZATION
    )

    graph_entities.extend(
        build_services()
    )

    graph_entities.extend(
        build_ports()
    )

    graph_entities.extend(
        build_corridors()
    )

    return {

        "@context":
        "https://schema.org",

        "@graph":
        graph_entities
    }


# ============================================================
# DATASET
# ============================================================

def build_dataset():

    return {

        "@context":
        "https://schema.org",

        "@type":
        "Dataset",

        "name":
        "The Flat Rate Movers Logistics Knowledge Graph",

        "description":
        (
            "Machine-readable logistics "
            "knowledge graph covering "
            "services, corridors, ports, "
            "counties, ZIP codes, transportation "
            "infrastructure, logistics workflows, "
            "and regional logistics intelligence."
        ),

        "creator":
        ORGANIZATION,

        "license":
        "MIT",

        "keywords": [

            "logistics graph",

            "container deconsolidation",

            "industrial crating",

            "export packing",

            "container loading",

            "container unloading",

            "transloading",

            "cross docking",

            "TWIC labor",

            "data center logistics",

            "IT equipment relocation",

            "Mid Atlantic logistics"
        ],

        "dateModified":
        datetime.utcnow().isoformat()
    }


# ============================================================
# DATA CATALOG
# ============================================================

def build_catalog():

    datasets = [

        {
            "@type": "Dataset",
            "name":
            "Regional Logistics Graph"
        },

        {
            "@type": "Dataset",
            "name":
            "Container Deconsolidation Graph"
        },

        {
            "@type": "Dataset",
            "name":
            "Technology Logistics Graph"
        },

        {
            "@type": "Dataset",
            "name":
            "Data Center Logistics Graph"
        }
    ]

    return {

        "@context":
        "https://schema.org",

        "@type":
        "DataCatalog",

        "name":
        "The Flat Rate Movers Logistics Knowledge Catalog",

        "description":
        (
            "Catalog of logistics "
            "datasets, ontologies, "
            "knowledge graphs, "
            "case studies, workflows, "
            "and transportation intelligence."
        ),

        "provider":
        ORGANIZATION,

        "dataset":
        datasets
    }


# ============================================================
# WRITE FILE
# ============================================================

def write_file(name, data):

    output_file = EXPORTS / name

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )

    print(
        f"EXPORTED: {name}"
    )


# ============================================================
# EXPORT ALL
# ============================================================

def export_all():

    write_file(
        "logistics-dataset.jsonld",
        build_dataset()
    )

    write_file(
        "logistics-datacatalog.jsonld",
        build_catalog()
    )

    write_file(
        "logistics-knowledge-graph.jsonld",
        build_knowledge_graph()
    )

    write_file(
        "logistics-services.jsonld",
        {
            "@context":
            "https://schema.org",
            "@graph":
            build_services()
        }
    )

    write_file(
        "logistics-ports.jsonld",
        {
            "@context":
            "https://schema.org",
            "@graph":
            build_ports()
        }
    )

    write_file(
        "logistics-corridors.jsonld",
        {
            "@context":
            "https://schema.org",
            "@graph":
            build_corridors()
        }
    )

    print(
        "JSON-LD EXPORT COMPLETE"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    export_all()
