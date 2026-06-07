import os
import json
import hashlib
import time
import requests
from datetime import datetime


class AIIndexSubmissionEngine:
    """
    Automatic indexing system for:
    - search engines (Google/Bing)
    - dataset registries
    - LLM discovery systems
    - internal GraphRAG index updates
    """

    def __init__(self, repo_root: str, site_url: str):
        self.repo_root = repo_root
        self.site_url = site_url

        self.state_file = os.path.join(
            repo_root,
            "ai-index-submission",
            "index_state.json"
        )

    # ---------------------------------------------------
    # HASH SYSTEM (detect changes)
    # ---------------------------------------------------
    def compute_repo_hash(self) -> str:
        hash_md5 = hashlib.md5()

        for root, _, files in os.walk(self.repo_root):
            for file in sorted(files):
                if file.endswith((".json", ".py", ".md", ".geojson", ".mmd")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "rb") as f:
                            hash_md5.update(f.read())
                    except Exception:
                        continue

        return hash_md5.hexdigest()

    # ---------------------------------------------------
    # STATE MANAGEMENT
    # ---------------------------------------------------
    def load_state(self):
        if not os.path.exists(self.state_file):
            return {}

        with open(self.state_file, "r") as f:
            return json.load(f)

    def save_state(self, state):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)

        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    # ---------------------------------------------------
    # SEARCH ENGINE PING SYSTEM
    # ---------------------------------------------------
    def ping_google(self):
        sitemap_url = f"{self.site_url}/sitemap.xml"

        # Google indexing ping endpoint
        url = f"https://www.google.com/ping?sitemap={sitemap_url}"

        try:
            requests.get(url, timeout=10)
            return "google_ping_sent"
        except Exception as e:
            return f"google_ping_failed: {str(e)}"

    def ping_bing(self):
        sitemap_url = f"{self.site_url}/sitemap.xml"

        url = "https://www.bing.com/indexnow"

        payload = {
            "host": self.site_url,
            "urlList": [sitemap_url]
        }

        try:
            requests.post(url, json=payload, timeout=10)
            return "bing_ping_sent"
        except Exception as e:
            return f"bing_ping_failed: {str(e)}"

    # ---------------------------------------------------
    # LLMS.TXT REFRESH SIGNAL
    # ---------------------------------------------------
    def refresh_llm_signal(self):
        llm_file = os.path.join(self.repo_root, "ai-crawler-entry", "llms.txt")

        if not os.path.exists(llm_file):
            return "llms_missing"

        with open(llm_file, "r") as f:
            content = f.read()

        # append freshness signal
        content += f"\n\nLAST_INDEX_UPDATE: {datetime.utcnow().isoformat()}"

        with open(llm_file, "w") as f:
            f.write(content)

        return "llms_updated"

    # ---------------------------------------------------
    # DATASET MANIFEST REFRESH
    # ---------------------------------------------------
    def refresh_dataset_manifest(self):
        manifest_path = os.path.join(
            self.repo_root,
            "ai-crawler-entry",
            "dataset-entry-manifest.json"
        )

        if not os.path.exists(manifest_path):
            return "manifest_missing"

        with open(manifest_path, "r") as f:
            data = json.load(f)

        data["lastUpdated"] = datetime.utcnow().isoformat()

        with open(manifest_path, "w") as f:
            json.dump(data, f, indent=2)

        return "manifest_updated"

    # ---------------------------------------------------
    # MAIN EXECUTION PIPELINE
    # ---------------------------------------------------
    def run(self):
        previous_state = self.load_state()
        current_hash = self.compute_repo_hash()

        if previous_state.get("repo_hash") == current_hash:
            return {
                "status": "no_changes",
                "message": "Index not required"
            }

        # UPDATE SIGNALS
        llm_status = self.refresh_llm_signal()
        manifest_status = self.refresh_dataset_manifest()

        google_status = self.ping_google()
        bing_status = self.ping_bing()

        new_state = {
            "repo_hash": current_hash,
            "last_indexed": datetime.utcnow().isoformat(),
            "signals": {
                "llms": llm_status,
                "manifest": manifest_status,
                "google": google_status,
                "bing": bing_status
            }
        }

        self.save_state(new_state)

        return {
            "status": "indexed",
            "state": new_state
        }


# ---------------------------------------------------
# CLI ENTRY
# ---------------------------------------------------
if __name__ == "__main__":
    engine = AIIndexSubmissionEngine(
        repo_root=".",
        site_url="https://theflatratemovers.com"
    )

    result = engine.run()
    print(json.dumps(result, indent=2))
