from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import uvicorn

from graph.vector_graph_rag_pipeline import VectorGraphRAGPipeline
from processors.live_event_graph_updater import LiveEventGraphUpdater


# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI(
    title="Flat Rate Movers GraphRAG API",
    description="AI retrieval + logistics graph reasoning system",
    version="1.0.0"
)


# -----------------------------
# GLOBAL STATE (IN-MEMORY GRAPH)
# -----------------------------
GRAPH_STATE = {
    "nodes": [],
    "edges": []
}


# -----------------------------
# LOADERS (BOOTSTRAP)
# -----------------------------
def load_graph(path: str):
    global GRAPH_STATE
    with open(path, "r") as f:
        GRAPH_STATE = json.load(f)


# -----------------------------
# VECTOR PIPELINE
# -----------------------------
vector_pipeline = VectorGraphRAGPipeline()


# -----------------------------
# EVENT ENGINE
# -----------------------------
event_engine = LiveEventGraphUpdater(GRAPH_STATE)


# -----------------------------
# REQUEST MODELS
# -----------------------------
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class EventRequest(BaseModel):
    event_type: str
    job_id: str
    payload: Dict[str, Any]


class NodeRequest(BaseModel):
    node_id: str


# -----------------------------
# SYSTEM BOOTSTRAP
# -----------------------------
@app.on_event("startup")
def startup():
    load_graph("graph_rag_output.json")

    vector_pipeline.ingest_graph(GRAPH_STATE)


# =========================================================
# 1. ROOT GRAPH ENTRY
# =========================================================
@app.get("/graph/root")
def get_root():
    for node in GRAPH_STATE["nodes"]:
        if node["id"] == "kg:root":
            return node

    raise HTTPException(status_code=404, detail="Root not found")


# =========================================================
# 2. NODE LOOKUP
# =========================================================
@app.post("/graph/node")
def get_node(req: NodeRequest):
    for node in GRAPH_STATE["nodes"]:
        if node["id"] == req.node_id:
            return node

    raise HTTPException(status_code=404, detail="Node not found")


# =========================================================
# 3. EDGE TRAVERSAL
# =========================================================
@app.get("/graph/edges/{node_id}")
def get_edges(node_id: str):
    results = []

    for edge in GRAPH_STATE["edges"]:
        if edge["source"] == node_id:
            results.append(edge)

    return {"node": node_id, "edges": results}


# =========================================================
# 4. VECTOR SEARCH (SEMANTIC RAG)
# =========================================================
@app.post("/search/semantic")
def semantic_search(req: SearchRequest):
    results = vector_pipeline.search(req.query, req.top_k)
    return {
        "query": req.query,
        "results": results
    }


# =========================================================
# 5. HYBRID GRAPH + VECTOR SEARCH
# =========================================================
@app.post("/search/hybrid")
def hybrid_search(req: SearchRequest):
    semantic_results = vector_pipeline.search(req.query, req.top_k)

    graph_results = []

    for item in semantic_results:
        node_id = item["id"]

        connected = [
            edge for edge in GRAPH_STATE["edges"]
            if edge["source"] == node_id or edge["target"] == node_id
        ]

        graph_results.append({
            "node_id": node_id,
            "text": item["text"],
            "connections": connected
        })

    return {
        "query": req.query,
        "semantic": semantic_results,
        "graph_context": graph_results
    }


# =========================================================
# 6. EVENT INGESTION (REAL-TIME LOGISTICS STATE)
# =========================================================
@app.post("/event/ingest")
def ingest_event(req: EventRequest):
    event = {
        "event_type": req.event_type,
        "job_id": req.job_id,
        "payload": req.payload
    }

    event_engine.process_event(event)

    return {
        "status": "processed",
        "event": event
    }


# =========================================================
# 7. LOGISTICS CONTEXT QUERY (AI READY ENDPOINT)
# =========================================================
@app.get("/ai/context/{query}")
def ai_context(query: str):

    semantic = vector_pipeline.search(query, 5)

    context_nodes = []

    for item in semantic:
        node_id = item["id"]

        related_edges = [
            e for e in GRAPH_STATE["edges"]
            if e["source"] == node_id or e["target"] == node_id
        ]

        context_nodes.append({
            "node": item,
            "graph_links": related_edges
        })

    return {
        "query": query,
        "context": context_nodes,
        "system": "GraphRAG Logistics Intelligence Engine"
    }


# =========================================================
# 8. HEALTH CHECK
# =========================================================
@app.get("/health")
def health():
    return {
        "status": "active",
        "nodes": len(GRAPH_STATE["nodes"]),
        "edges": len(GRAPH_STATE["edges"]),
        "system": "Flat Rate Movers GraphRAG API"
    }


# -----------------------------
# MAIN RUN
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "api.graphrag_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
