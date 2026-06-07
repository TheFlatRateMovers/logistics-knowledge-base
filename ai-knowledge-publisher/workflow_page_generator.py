import os
import json
from datetime import datetime


class WorkflowPageGenerator:

    def __init__(self, workflow_dir: str, output_dir: str):
        self.workflow_dir = workflow_dir
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def load_files(self):
        workflows = []

        for file in os.listdir(self.workflow_dir):
            if file.endswith(".json") or file.endswith(".md"):
                path = os.path.join(self.workflow_dir, file)

                with open(path, "r", encoding="utf-8") as f:
                    workflows.append((file, f.read()))

        return workflows

    def render(self, name, content):

        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{name} | Logistics Workflow</title>
    <meta name="robots" content="index, follow">
</head>

<body>

<h1>{name}</h1>

<h2>Workflow Content</h2>
<pre>{content}</pre>

<h2>AI Context</h2>
<p>
This workflow is part of a structured logistics system covering
export packing, freight handling, and container operations.
</p>

</body>
</html>
"""

    def generate(self):
        workflows = self.load_files()

        for name, content in workflows:

            safe = name.replace(" ", "_")
            file_path = os.path.join(self.output_dir, safe + ".html")

            html = self.render(name, content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

        return len(workflows)


if __name__ == "__main__":
    gen = WorkflowPageGenerator(
        workflow_dir="./workflow",
        output_dir="./ai-site/workflows"
    )

    print("Generated workflows:", gen.generate())
