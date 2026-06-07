import json
from typing import Dict, Any, List
from neo4j import GraphDatabase


class Neo4jGraphLoader:
    """
    Loads GraphRAG output into Neo4j for The Flat Rate Movers Logistics Knowledge Base.
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # -----------------------------
    # CREATE NODE
    # -----------------------------
    def create_node(self, tx, node: Dict[str, Any]):
        query = """
        MERGE (n:Entity {id: $id})
        SET n.type = $type,
            n += $properties
        """
        tx.run(query, id=node["id"], type=node["type"], properties=node["properties"])

    # -----------------------------
    # CREATE EDGE
    # -----------------------------
    def create_edge(self, tx, edge: Dict[str, Any]):
        query = """
        MATCH (a:Entity {id: $source})
        MATCH (b:Entity {id: $target})
        MERGE (a)-[:RELATES {type: $relation}]->(b)
        """
        tx.run(
            query,
            source=edge["source"],
            target=edge["target"],
            relation=edge["relation"]
        )

    # -----------------------------
    # LOAD GRAPH
    # -----------------------------
    def load_graph(self, graph: Dict[str, Any]):
        with self.driver.session() as session:

            for node in graph.get("nodes", []):
                session.execute_write(self.create_node, node)

            for edge in graph.get("edges", []):
                session.execute_write(self.create_edge, edge)

    def close(self):
        self.driver.close()


# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    import sys

    graph_file = sys.argv[1]

    loader = Neo4jGraphLoader(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    with open(graph_file, "r") as f:
        graph = json.load(f)

    loader.load_graph(graph)
    loader.close()

    print("[Neo4j] Graph loaded successfully.")
