import json
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np


class VectorGraphRAGPipeline:
    """
    Converts graph nodes into embeddings for semantic retrieval.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_store = []

    # -----------------------------
    # FLATTEN NODE TEXT
    # -----------------------------
    def node_to_text(self, node: Dict[str, Any]) -> str:
        return f"{node['type']} | {node.get('id')} | {json.dumps(node.get('properties', {}))}"

    # -----------------------------
    # INGEST GRAPH
    # -----------------------------
    def ingest_graph(self, graph: Dict[str, Any]):
        for node in graph.get("nodes", []):
            text = self.node_to_text(node)
            embedding = self.model.encode(text)

            self.vector_store.append({
                "id": node["id"],
                "embedding": embedding,
                "text": text
            })

    # -----------------------------
    # SEARCH
    # -----------------------------
    def search(self, query: str, top_k: int = 5):
        query_vec = self.model.encode(query)

        scored = []

        for item in self.vector_store:
            score = np.dot(query_vec, item["embedding"])
            scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [x[1] for x in scored[:top_k]]
