from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID
import uvicorn

from graph.graphrag_ingestion_engine import GraphRAGIngestionEngine
from graph.vector_graph_rag_pipeline import VectorGraphRAGPipeline
from processors.live_event_graph_updater import LiveEventGraphUpdater
from processors.schema_validator import validate_event
from state.current_state_store import STATE_STORE


app = FastAPI(
    title="Flat Rate Movers GraphRAG API",
    description="AI retrieval + logistics graph reasoning system",
    version="1.1.1"
)

GRAPH_STATE: Dict[str, Any] = {"nodes": [], "edges": []}
vector_pipeline = VectorGraphRAGPipeline()
event_engine = LiveEventGraphUpdater(GRAPH_STATE)


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)


class EventRequest(BaseModel):
    eventId: UUID
    eventType: str
    eventVersion: str = "1.0.0"
    eventTimestamp: str
    eventSource: str
    entityType: str
    entityId: str
    correlationId: str
    causationId: Optional[str] = None
    stateTransition: Dict[str, str]
    payload: Dict[str, Any] = Field(default_factory=dict)
    serviceCategory: Optional[str] = None
    serviceTerritory: Optional[Dict[str, Any]] = None
    businessEntity: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class NodeRequest(BaseModel):
    node_id: str


def build_graph():
    return GraphRAGIngestionEngine(".").run()


@app.on_event("startup")
def startup():
    global GRAPH_STATE, event_engine
    GRAPH_STATE = build_graph()
    event_engine = LiveEventGraphUpdater(GRAPH_STATE)
    vector_pipeline.ingest_graph(GRAPH_STATE)


@app.get("/graph/root")
def get_root():
    for node in GRAPH_STATE["nodes"]:
        if node["id"] == "kg:root":
            return node
    raise HTTPException(status_code=404, detail="Root not found")


@app.post("/graph/node")
def get_node(req: NodeRequest):
    for node in GRAPH_STATE["nodes"]:
        if node["id"] == req.node_id:
            return node
    raise HTTPException(status_code=404, detail="Node not found")


@app.get("/graph/edges/{node_id}")
def get_edges(node_id: str):
    return {"node": node_id, "edges": [edge for edge in GRAPH_STATE["edges"] if edge["source"] == node_id or edge["target"] == node_id]}


@app.post("/search/semantic")
def semantic_search(req: SearchRequest):
    return {"query": req.query, "results": vector_pipeline.search(req.query, req.top_k)}


@app.post("/search/hybrid")
def hybrid_search(req: SearchRequest):
    semantic_results = vector_pipeline.search(req.query, req.top_k)
    graph_results = []
    for item in semantic_results:
        node_id = item["id"]
        connected = [edge for edge in GRAPH_STATE["edges"] if edge["source"] == node_id or edge["target"] == node_id]
        graph_results.append({"node_id": node_id, "text": item["text"], "connections": connected})
    return {"query": req.query, "semantic": semantic_results, "graph_context": graph_results}


@app.post("/event/ingest")
def ingest_event(req: EventRequest):
    event = req.model_dump(mode="json") if hasattr(req, "model_dump") else req.dict()
    try:
        validate_event(event)
        state = STATE_STORE.apply_event(event)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    projection = event_engine.process_event(event)
    STATE_STORE.save_state()
    return {"status": "processed", "event": event, "state": state, "projection": projection}


@app.get("/state/{entity_id}")
def get_state(entity_id: str):
    state = STATE_STORE.get_job(entity_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Job state not found")
    return state


@app.get("/ai/context/{query}")
def ai_context(query: str):
    semantic = vector_pipeline.search(query, 5)
    context_nodes = []
    for item in semantic:
        node_id = item["id"]
        related_edges = [edge for edge in GRAPH_STATE["edges"] if edge["source"] == node_id or edge["target"] == node_id]
        context_nodes.append({"node": item, "graph_links": related_edges})
    return {"query": query, "context": context_nodes, "system": "GraphRAG Logistics Intelligence Engine"}


@app.get("/health")
def health():
    return {"status": "active", "nodes": len(GRAPH_STATE["nodes"]), "edges": len(GRAPH_STATE["edges"]), "system": "Flat Rate Movers GraphRAG API", "canonicalRoot": "/repository-index/root-pointer.json"}


if __name__ == "__main__":
    uvicorn.run("api.graphrag_server:app", host="0.0.0.0", port=8000, reload=True)
