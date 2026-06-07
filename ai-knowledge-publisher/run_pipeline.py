from entity_page_generator import EntityPageGenerator
from workflow_page_generator import WorkflowPageGenerator
from sitemap_generator import SitemapGenerator


def run_all():

    print("\n[1] Generating Entity Pages...")
    e = EntityPageGenerator(
        graph_path="graph_rag_output.json",
        output_dir="./ai-site/entities"
    )
    print("Entities:", e.generate())

    print("\n[2] Generating Workflow Pages...")
    w = WorkflowPageGenerator(
        workflow_dir="./workflow",
        output_dir="./ai-site/workflows"
    )
    print("Workflows:", w.generate())

    print("\n[3] Generating Sitemap...")
    s = SitemapGenerator(
        base_url="https://theflatratemovers.com",
        site_dir="./ai-site"
    )
    print("Sitemap URLs:", s.generate())

    print("\n[AI Knowledge Publisher] COMPLETE")


if __name__ == "__main__":
    run_all()
