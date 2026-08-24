"""Graph access API for the logistics knowledge graph."""
from fastapi import FastAPI

app = FastAPI(title="Graph API", version="1.1.0")

# Runtime graph data can be injected by the GraphRAG service.
GRAPH = {"nodes": [], "relationships": []}

@app.get("/")
def root():
    return {"service": "Graph API", "version": "1.1.0", "status": "active"}

@app.get("/nodes")
def list_nodes():
    return {"node_count": len(GRAPH["nodes"]), "nodes": GRAPH["nodes"]}

@app.get("/relationships")
def list_relationships():
    return {"relationship_count": len(GRAPH["relationships"]), "relationships": GRAPH["relationships"]}

@app.get("/node/{node_id}")
def get_node(node_id: str):
    for node in GRAPH["nodes"]:
        if node.get("id") == node_id or node.get("node_id") == node_id:
            return node
    return {"node_id": node_id, "found": False}

@app.get("/graph/search")
def graph_search(query: str):
    q = query.lower()
    results = [node for node in GRAPH["nodes"] if q in str(node).lower()]
    return {"query": query, "results": results}

@app.get("/graph/subgraph/{entity_id}")
def entity_subgraph(entity_id: str):
    related = [edge for edge in GRAPH["relationships"] if edge.get("source") == entity_id or edge.get("target") == entity_id]
    return {"entity_id": entity_id, "nodes": [n for n in GRAPH["nodes"] if n.get("id") == entity_id], "relationships": related}

@app.get("/graph/path")
def shortest_path(source: str, target: str):
    return {"source": source, "target": target, "path": []}
