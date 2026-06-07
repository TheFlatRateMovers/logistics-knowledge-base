import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class GraphRAGIngestionEngine:
    """
    Core ingestion engine for The Flat Rate Movers Logistics Knowledge Base.

    Converts:
    - JSON-LD machine indexing registry
    - root pointer graph
    - ontology schemas
    - datasets
    - event streams

    Into a unified GraphRAG-compatible representation.
    """

    def __init__(self, repo_root: str):
        self.repo_root = repo_root

        self.root_pointer_path = os.path.join(
            repo_root,
            "repository-index",
            "root-pointer.v2.json"
        )

        self.index_registry_path = os.path.join(
            repo_root,
            "repository-index",
            "machine-indexing.registry.v2.jsonld"
        )

        self.output_graph = {
            "nodes": [],
            "edges": [],
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "source": "GraphRAGIngestionEngine",
                "system": "FlatRateMoversLogisticsKnowledgeBase"
            }
        }

        self.node_index = set()

    # -----------------------------
    # LOADERS
    # -----------------------------

    def load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_system_assets(self):
        self.root_pointer = self.load_json(self.root_pointer_path)
        self.index_registry = self.load_json(self.index_registry_path)

    # -----------------------------
    # NODE CREATION
    # -----------------------------

    def add_node(self, node_id: str, node_type: str, properties: Dict[str, Any]):
        if node_id in self.node_index:
            return

        node = {
            "id": node_id,
            "type": node_type,
            "properties": properties
        }

        self.output_graph["nodes"].append(node)
        self.node_index.add(node_id)

    def add_edge(self, source: str, target: str, relation: str):
        edge = {
            "source": source,
            "target": target,
            "relation": relation
        }

        self.output_graph["edges"].append(edge)

    # -----------------------------
    # ROOT PROCESSING
    # -----------------------------

    def ingest_root_pointer(self):
        root = self.root_pointer

        root_id = root.get("@id", "kg:root")

        self.add_node(
            node_id=root_id,
            node_type="KnowledgeGraphRoot",
            properties={
                "name": root.get("name"),
                "description": root.get("description"),
                "organization": root.get("organization"),
                "ai_ready": root.get("AIReadiness", {}),
            }
        )

        # Bind system components
        bindings = root.get("systemBindings", {})

        for key, path in bindings.items():
            node_id = f"system:{key}"

            self.add_node(
                node_id=node_id,
                node_type="SystemComponent",
                properties={
                    "path": path,
                    "role": key
                }
            )

            self.add_edge(root_id, node_id, "HAS_SYSTEM_COMPONENT")

    # -----------------------------
    # INDEX REGISTRY PROCESSING
    # -----------------------------

    def ingest_index_registry(self):
        index = self.index_registry

        index_id = index.get("@id", "kg:index")

        self.add_node(
            node_id=index_id,
            node_type="MachineIndex",
            properties={
                "name": index.get("name"),
                "keywords": index.get("keywords", []),
                "geo_scope": index.get("spatialCoverage"),
                "time_scope": index.get("temporalCoverage")
            }
        )

        # Link to root
        self.add_edge("kg:root", index_id, "HAS_MACHINE_INDEX")

        # Bind dataset scopes
        for scope in index.get("datasetScope", []):
            scope_id = f"scope:{scope.replace(' ', '_')}"

            self.add_node(
                node_id=scope_id,
                node_type="DatasetScope",
                properties={"name": scope}
            )

            self.add_edge(index_id, scope_id, "COVERS_DOMAIN")

    # -----------------------------
    # EVENT SYSTEM INGESTION
    # -----------------------------

    def ingest_event_schema(self):
        event_router_path = os.path.join(
            self.repo_root,
            "processors",
            "event_router.py"
        )

        state_path = os.path.join(
            self.repo_root,
            "state",
            "current_state_store.py"
        )

        self.add_node(
            "system:event_router",
            "EventRouter",
            {"path": event_router_path}
        )

        self.add_node(
            "system:state_store",
            "StateStore",
            {"path": state_path}
        )

        self.add_edge("kg:root", "system:event_router", "HAS_EVENT_SYSTEM")
        self.add_edge("system:event_router", "system:state_store", "UPDATES")

    # -----------------------------
    # DATASET INGESTION (GENERIC)
    # -----------------------------

    def ingest_datasets(self):
        dataset_dir = os.path.join(self.repo_root, "datasets")

        if not os.path.exists(dataset_dir):
            return

        for file in os.listdir(dataset_dir):
            if file.endswith(".json"):
                path = os.path.join(dataset_dir, file)

                try:
                    data = self.load_json(path)
                except Exception:
                    continue

                node_id = f"dataset:{file}"

                self.add_node(
                    node_id=node_id,
                    node_type="Dataset",
                    properties={
                        "file": file,
                        "keys": list(data.keys()) if isinstance(data, dict) else "array",
                        "size": len(data) if isinstance(data, list) else None
                    }
                )

                self.add_edge("kg:root", node_id, "HAS_DATASET")

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------

    def run(self) -> Dict[str, Any]:
        self.load_system_assets()

        self.ingest_root_pointer()
        self.ingest_index_registry()
        self.ingest_event_schema()
        self.ingest_datasets()

        return self.output_graph

    # -----------------------------
    # EXPORT
    # -----------------------------

    def export(self, output_path: str):
        graph = self.run()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2)

        return output_path


# -----------------------------
# CLI EXECUTION
# -----------------------------

if __name__ == "__main__":
    import sys

    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "graph_rag_output.json"

    engine = GraphRAGIngestionEngine(repo_root)
    path = engine.export(output_file)

    print(f"[GraphRAG] Export complete → {path}")
