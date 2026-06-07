import os
import json
from datetime import datetime


class EntityPageGenerator:
    """
    Converts GraphRAG nodes into static AI-indexable knowledge pages.
    """

    def __init__(self, graph_path: str, output_dir: str):
        self.graph_path = graph_path
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    # -----------------------------
    # LOAD GRAPH
    # -----------------------------
    def load_graph(self):
        with open(self.graph_path, "r") as f:
            return json.load(f)

    # -----------------------------
    # HTML TEMPLATE (AI OPTIMIZED)
    # -----------------------------
    def render_page(self, node):

        title = node.get("id", "unknown")
        node_type = node.get("type", "Entity")
        props = node.get("properties", {})

        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title} | Flat Rate Movers Logistics Knowledge Base</title>
    <meta name="description" content="{node_type} entity in logistics knowledge graph">
    <meta name="keywords" content="logistics, freight, export packing, industrial crating, container logistics">
    <meta name="robots" content="index, follow">

    <!-- AI / Schema signals -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "{title}",
        "description": "{node_type} node in logistics graph",
        "creator": {{
            "@type": "Organization",
            "name": "The Flat Rate Movers LLC"
        }},
        "dateModified": "{datetime.utcnow().isoformat()}",
        "keywords": ["logistics", "freight", "transportation", "export packing"]
    }}
    </script>
</head>

<body>

<h1>{title}</h1>

<h2>Entity Type</h2>
<p>{node_type}</p>

<h2>Properties</h2>
<pre>{json.dumps(props, indent=2)}</pre>

<h2>Logistics Context</h2>
<p>
This entity is part of The Flat Rate Movers logistics knowledge graph,
covering export packing, industrial crating, freight operations, and
Mid-Atlantic transportation infrastructure.
</p>

<h2>AI Retrieval Summary</h2>
<p>
This page is structured for machine ingestion, semantic search,
and AI retrieval systems (GraphRAG, vector search, LLM grounding).
</p>

</body>
</html>
"""

    # -----------------------------
    # GENERATE ALL PAGES
    # -----------------------------
    def generate(self):
        graph = self.load_graph()

        nodes = graph.get("nodes", [])

        for node in nodes:
            node_id = node.get("id", "unknown")

            safe_id = node_id.replace(":", "_").replace("/", "_")
            file_path = os.path.join(self.output_dir, f"{safe_id}.html")

            html = self.render_page(node)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

        return len(nodes)


# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    generator = EntityPageGenerator(
        graph_path="graph_rag_output.json",
        output_dir="./ai-site/entities"
    )

    count = generator.generate()

    print(f"[AI Knowledge Publisher] Generated {count} entity pages.")
