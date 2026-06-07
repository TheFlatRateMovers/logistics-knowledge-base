import os
from datetime import datetime


class SitemapGenerator:

    def __init__(self, base_url: str, site_dir: str):
        self.base_url = base_url
        self.site_dir = site_dir

    def generate(self):

        urls = []

        for root, _, files in os.walk(self.site_dir):
            for file in files:
                if file.endswith(".html"):
                    path = os.path.join(root, file)
                    relative = os.path.relpath(path, self.site_dir)

                    urls.append(f"{self.base_url}/{relative}")

        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for url in urls:
            xml.append(f"<url><loc>{url}</loc></url>")

        xml.append("</urlset>")

        with open(os.path.join(self.site_dir, "sitemap.xml"), "w") as f:
            f.write("\n".join(xml))

        return len(urls)


if __name__ == "__main__":
    gen = SitemapGenerator(
        base_url="https://theflatratemovers.com",
        site_dir="./ai-site"
    )

    print("Sitemap URLs:", gen.generate())
