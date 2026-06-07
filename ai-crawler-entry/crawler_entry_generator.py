import json
from datetime import datetime


class CrawlerEntryGenerator:

    def generate_manifest(self):
        return {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "name": "Flat Rate Movers Logistics Knowledge Base",
            "updated": datetime.utcnow().isoformat(),
            "status": "machine-readable-active"
        }

    def write(self, path="dataset-entry-manifest.json"):
        data = self.generate_manifest()

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        return path


if __name__ == "__main__":
    gen = CrawlerEntryGenerator()
    print("Generated:", gen.write())
