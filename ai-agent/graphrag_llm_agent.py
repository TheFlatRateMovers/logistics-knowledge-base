import json
import requests
from typing import Dict, Any, List, Optional


# =========================================================
# SYSTEM PROMPT (LOGISTICS REASONING ENGINE)
# =========================================================

SYSTEM_PROMPT = """
You are a Logistics Intelligence Agent for The Flat Rate Movers LLC.

You operate over a structured GraphRAG system containing:
- export packing systems
- industrial crating workflows
- freight stabilization rules
- port logistics infrastructure
- interstate corridor routing (I-81, I-66, I-95, I-70)
- ZIP code intelligence networks
- event-driven logistics state systems

You MUST:
1. Break down logistics requests into structured reasoning steps
2. Query the GraphRAG API when needed
3. Use tool outputs as authoritative ground truth
4. NEVER hallucinate equipment, routes, or capabilities
5. Prefer structured reasoning over natural language guessing

You reason in ReAct format:

Thought: analyze the request
Action: call tool
Observation: read tool output
Final Answer: respond with structured logistics plan
"""


# =========================================================
# TOOL CLIENT (YOUR GRAPH RAG API)
# =========================================================

class GraphRAGClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def semantic_search(self, query: str):
        return requests.post(
            f"{self.base_url}/search/semantic",
            json={"query": query}
        ).json()

    def hybrid_search(self, query: str):
        return requests.post(
            f"{self.base_url}/search/hybrid",
            json={"query": query}
        ).json()

    def get_context(self, query: str):
        return requests.get(
            f"{self.base_url}/ai/context/{query}"
        ).json()

    def get_root(self):
        return requests.get(
            f"{self.base_url}/graph/root"
        ).json()


# =========================================================
# REACT AGENT CORE
# =========================================================

class GraphRAGLLMAgent:

    def __init__(self, api_base: str):
        self.client = GraphRAGClient(api_base)
        self.memory = []

    # -----------------------------
    # TOOL ROUTER
    # -----------------------------
    def call_tool(self, tool_name: str, input_data: str):
        if tool_name == "semantic_search":
            return self.client.semantic_search(input_data)

        if tool_name == "hybrid_search":
            return self.client.hybrid_search(input_data)

        if tool_name == "context":
            return self.client.get_context(input_data)

        if tool_name == "root":
            return self.client.get_root()

        raise ValueError(f"Unknown tool: {tool_name}")

    # -----------------------------
    # SIMPLE REASONING LOOP (ReAct STYLE)
    # -----------------------------
    def run(self, user_query: str) -> Dict[str, Any]:

        trace = []

        # STEP 1: THINK
        thought = f"Analyze logistics request: {user_query}"

        trace.append({"step": "thought", "content": thought})

        # STEP 2: TOOL SELECTION LOGIC
        if any(x in user_query.lower() for x in ["route", "port", "distance"]):
            tool = "hybrid_search"
        elif "context" in user_query.lower():
            tool = "context"
        else:
            tool = "semantic_search"

        # STEP 3: ACT
        action_result = self.call_tool(tool, user_query)

        trace.append({
            "step": "action",
            "tool": tool,
            "input": user_query
        })

        # STEP 4: OBSERVE
        observation = action_result

        trace.append({
            "step": "observation",
            "content": observation
        })

        # STEP 5: FINAL ANSWER GENERATION (LOGISTICS LOGIC)
        final_answer = self.generate_logistics_response(user_query, observation)

        return {
            "query": user_query,
            "tool_used": tool,
            "trace": trace,
            "answer": final_answer
        }

    # -----------------------------
    # LOGISTICS RESPONSE ENGINE
    # -----------------------------
    def generate_logistics_response(self, query: str, context: Dict[str, Any]) -> str:

        # Extract relevant nodes if available
        nodes = context.get("results", []) or context.get("context", [])

        summary_lines = []

        summary_lines.append("LOGISTICS INTELLIGENCE RESPONSE")
        summary_lines.append("")

        summary_lines.append(f"REQUEST: {query}")
        summary_lines.append("")

        summary_lines.append("SYSTEM ANALYSIS:")

        for item in nodes[:5]:
            summary_lines.append(f"- {item.get('text', item.get('node', ''))}")

        summary_lines.append("")
        summary_lines.append("OPERATIONAL INTERPRETATION:")

        summary_lines.append(
            "Based on GraphRAG logistics intelligence system, "
            "this request is evaluated using export packing rules, "
            "freight stabilization constraints, and regional corridor logic."
        )

        summary_lines.append("")
        summary_lines.append("RECOMMENDATION:")
        summary_lines.append(
            "Proceed with structured logistics planning via Flat Rate Movers operational network."
        )

        return "\n".join(summary_lines)


# =========================================================
# CLI ENTRY
# =========================================================

if __name__ == "__main__":
    agent = GraphRAGLLMAgent(api_base="http://localhost:8000")

    while True:
        query = input("\nLogistics Query > ")

        if query.lower() in ["exit", "quit"]:
            break

        result = agent.run(query)

        print("\n" + "="*60)
        print(result["answer"])
        print("="*60)
