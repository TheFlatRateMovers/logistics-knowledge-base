import os
import json
from typing import Dict, Any
from datetime import datetime, timezone


class GraphRAGIngestionEngine:
    """Builds a deterministic GraphRAG representation from canonical repository assets."""

    def __init__(self, repo_root: str):
        self.repo_root = os.path.abspath(repo_root)
        self.root_pointer_path = os.path.join(
            self.repo_root, "repository-index", "root-pointer.json"
        )
        self.index_registry_path = os.path.join(
            self.repo_root, "repository-index", "machine-indexing.registry.jsonld"
        )
        self.output_graph = {
            "nodes": [],
            "edges": [],
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source": "GraphRAGIngestionEngine",
                "system": "FlatRateMoversLogisticsKnowledgeBase",
                "canonicalRoot": "/repository-index/root-pointer.json",
                "canonicalRegistry": "/repository-index/machine-indexing.registry.jsonld"
            }
        }
        self.node_index = set()

    def load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def load_system_assets(self):
        self.root_pointer = self.load_json(self.root_pointer_path)
        self.index_registry = self.load_json(self.index_registry_path)

    def add_node(self, node_id: str, node_type: str, properties: Dict[str, Any]):
        if node_id in self.node_index:
            return
        self.output_graph["nodes"].append({
            "id": node_id,
            "type": node_type,
            "properties": properties
        })
        self.node_index.add(node_id)

    def add_edge(self, source: str, target: str, relation: str):
        self.output_graph["edges"].append({
            "source": source,
            "target": target,
            "relation": relation
        })

    def ingest_root_pointer(self):
        root = self.root_pointer
        root_id = root.get("@id", "kg:root")
        self.add_node(root_id, "KnowledgeGraphRoot", {
            "name": root.get("name"),
            "description": root.get("description"),
            "organization": root.get("organization"),
            "ai_ready": root.get("aiIntegrationLayer", root.get("AIReadiness", {})),
            "status": root.get("status"),
            "version": root.get("version")
        })

        bindings = root.get("canonicalDiscovery", {})
        for key, path in bindings.items():
            node_id = f"system:discovery:{key}"
            self.add_node(node_id, "SystemComponent", {"path": path, "role": key})
            self.add_edge(root_id, node_id, "HAS_CANONICAL_DISCOVERY")

        entry_points = root.get("entryPoints", {})
        for key, path in entry_points.items():
            node_id = f"system:entry:{key}"
            self.add_node(node_id, "SystemComponent", {"path": path, "role": key})
            self.add_edge(root_id, node_id, "HAS_ENTRY_POINT")

    def ingest_index_registry(self):
        index = self.index_registry
        index_id = index.get("@id", "kg:index")
        self.add_node(index_id, "MachineIndex", {
            "name": index.get("name"),
            "keywords": index.get("keywords", []),
            "geo_scope": index.get("spatialCoverage"),
            "time_scope": index.get("temporalCoverage")
        })
        self.add_edge("kg:root", index_id, "HAS_MACHINE_INDEX")
        for scope in index.get("datasetScope", []):
            scope_id = f"scope:{scope.replace(' ', '_')}"
            self.add_node(scope_id, "DatasetScope", {"name": scope})
            self.add_edge(index_id, scope_id, "COVERS_DOMAIN")

    def ingest_event_system(self):
        router = os.path.join(self.repo_root, "processors", "event_router.py")
        validator = os.path.join(self.repo_root, "processors", "schema_validator.py")
        state = os.path.join(self.repo_root, "state", "current_state_store.py")
        registry = os.path.join(self.repo_root, "protocol", "event-registry.json")
        for node_id, node_type, path in [
            ("system:event_router", "EventRouter", router),
            ("system:event_validator", "EventValidator", validator),
            ("system:state_store", "StateStore", state),
            ("system:event_registry", "EventRegistry", registry),
        ]:
            self.add_node(node_id, node_type, {"path": path})
        self.add_edge("kg:root", "system:event_registry", "HAS_EVENT_REGISTRY")
        self.add_edge("system:event_registry", "system:event_validator", "DRIVES_VALIDATION")
        self.add_edge("system:event_validator", "system:event_router", "VALIDATES_FOR")
        self.add_edge("system:event_router", "system:state_store", "UPDATES")

    def ingest_datasets(self):
        dataset_dir = os.path.join(self.repo_root, "datasets")
        if not os.path.exists(dataset_dir):
            return
        for file in sorted(os.listdir(dataset_dir)):
            if not file.endswith(".json"):
                continue
            path = os.path.join(dataset_dir, file)
            try:
                data = self.load_json(path)
            except Exception:
                continue
            node_id = f"dataset:{file}"
            self.add_node(node_id, "Dataset", {
                "file": file,
                "keys": list(data.keys()) if isinstance(data, dict) else "array",
                "size": len(data) if isinstance(data, list) else None
            })
            self.add_edge("kg:root", node_id, "HAS_DATASET")

    def run(self) -> Dict[str, Any]:
        self.load_system_assets()
        self.ingest_root_pointer()
        self.ingest_index_registry()
        self.ingest_event_system()
        self.ingest_datasets()
        return self.output_graph

    def export(self, output_path: str):
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(self.run(), handle, indent=2)
        return output_path


if __name__ == "__main__":
    import sys
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "graph_rag_output.json"
    print(f"[GraphRAG] Export complete → {GraphRAGIngestionEngine(repo_root).export(output_file)}")
