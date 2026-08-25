#!/usr/bin/env python3
"""Build a deterministic repository manifest from the current checkout."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "repository-manifest"
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}
TEXT_EXTENSIONS = {".md", ".markdown", ".py", ".json", ".jsonld", ".yaml", ".yml", ".toml", ".txt", ".html", ".css", ".js", ".ts", ".tsx", ".jsx", ".sh"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_tracked() -> set[str]:
    try:
        result = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True)
        return {x for x in result.stdout.splitlines() if x}
    except (OSError, subprocess.CalledProcessError):
        return set()


def classify(path: Path) -> str:
    p = rel(path).lower()
    name = path.name.lower()
    if p.startswith("repository-manifest/"):
        return "generated"
    if p.startswith("tools/") or p.startswith(".github/workflows/"):
        return "runtime"
    if any(x in p for x in ("deprecated", "archive", "legacy")):
        return "deprecated"
    if any(x in p for x in ("generated", "build", "dist", "output", "vector-index")):
        return "generated"
    if p.startswith(("docs/", "documentation/")) or path.suffix.lower() in {".md", ".markdown"}:
        return "documentation"
    if any(x in p for x in ("experiment", "prototype", "sandbox")):
        return "experimental"
    if any(x in p for x in ("ontology/", "datasets/", "schemas/", "protocols/", "glossaries/", "geojson/", "case-studies/", "faq/", "compliance/", "equipment/", "infrastructure/")):
        return "canonical"
    return "unknown"


def purpose(path: Path) -> str:
    p = rel(path)
    if p == "README.md":
        return "Repository entry documentation"
    if p.startswith("tools/"):
        return "Repository engineering automation"
    if p.startswith("repository-manifest/"):
        return "Repository stabilization metadata"
    if p.startswith(".github/workflows/"):
        return "Continuous integration workflow"
    if path.suffix.lower() in {".json", ".jsonld", ".yaml", ".yml"}:
        return "Structured data or configuration"
    if path.suffix.lower() in {".py", ".js", ".ts", ".tsx", ".jsx"}:
        return "Executable source code"
    if path.suffix.lower() in {".md", ".markdown", ".txt"}:
        return "Documentation or textual knowledge asset"
    return "Unclassified repository asset"


def python_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return []
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return sorted(found)


def text_references(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    refs: set[str] = set()
    patterns = [r"(?:\]\(|\"|')((?:\.\.?/|/)?[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+)", r"\$ref\s*:\s*['\"]([^'\"]+)['\"]"]
    for pattern in patterns:
        for match in re.findall(pattern, text):
            candidate = match.split("#", 1)[0].strip()
            if candidate and not candidate.startswith(("http://", "https://")):
                refs.add(candidate)
    return sorted(refs)


def census() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    tracked = git_tracked()
    files: list[dict[str, Any]] = []
    extension_counts: dict[str, int] = defaultdict(int)
    status_counts: dict[str, int] = defaultdict(int)
    dependency_edges: list[dict[str, str]] = []
    missing_refs: list[dict[str, str]] = []
    all_paths: set[str] = set()

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in IGNORE_DIRS for part in path.parts):
            continue
        rp = rel(path)
        all_paths.add(rp)
        status = classify(path)
        ext = path.suffix.lower() or "[no extension]"
        extension_counts[ext] += 1
        status_counts[status] += 1
        record: dict[str, Any] = {
            "path": rp,
            "name": path.name,
            "extension": ext,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "tracked": rp in tracked,
            "status": status,
            "purpose": purpose(path),
            "runtime": status == "runtime",
            "documentation": status == "documentation",
            "canonical": status == "canonical",
            "generated": status == "generated",
            "deprecated": status == "deprecated",
        }
        if path.suffix.lower() == ".py":
            record["python_imports"] = python_imports(path)
        refs = text_references(path)
        record["references"] = refs
        for target in refs:
            if target.startswith("#"):
                continue
            base = Path(rp).parent / target
            normalized = base.as_posix().lstrip("./")
            candidates = {normalized, f"{normalized}.md", f"{normalized}.json", f"{normalized}.jsonld", f"{normalized}.py"}
            if not any(c in all_paths for c in candidates):
                missing_refs.append({"source": rp, "reference": target})
            else:
                resolved = next(c for c in candidates if c in all_paths)
                dependency_edges.append({"source": rp, "target": resolved, "kind": "local-reference"})
        files.append(record)

    duplicate_hashes: dict[str, list[str]] = defaultdict(list)
    duplicate_names: dict[str, list[str]] = defaultdict(list)
    for f in files:
        duplicate_hashes[f["sha256"]].append(f["path"])
        duplicate_names[f["name"]].append(f["path"])
    duplicate_hashes = {k: v for k, v in duplicate_hashes.items() if len(v) > 1}
    duplicate_names = {k: v for k, v in duplicate_names.items() if len(v) > 1}

    repo = {
        "manifest_version": "1.0.0",
        "repository": "TheFlatRateMovers/logistics-knowledge-base",
        "generated_by": "tools/repository_census.py",
        "tracked_file_count": len(tracked),
        "scanned_file_count": len(files),
        "extension_inventory": dict(sorted(extension_counts.items())),
        "status_inventory": dict(sorted(status_counts.items())),
        "integrity": {
            "missing_local_references": len(missing_refs),
            "duplicate_content_groups": len(duplicate_hashes),
            "duplicate_filename_groups": len(duplicate_names),
        },
    }
    registry = {"manifest_version": "1.0.0", "files": files}
    deps = {"manifest_version": "1.0.0", "edges": dependency_edges, "missing_references": missing_refs}
    return repo, registry, deps


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when generated files differ from the committed baseline")
    args = parser.parse_args()
    repo, registry, deps = census()
    generated = {
        "repository-manifest.json": repo,
        "file-registry.json": registry,
        "dependency-registry.json": deps,
        "canonical-assets.json": {"assets": [f["path"] for f in registry["files"] if f["canonical"]]},
        "generated-assets.json": {"assets": [f["path"] for f in registry["files"] if f["generated"]]},
        "runtime-assets.json": {"assets": [f["path"] for f in registry["files"] if f["runtime"]]},
        "deprecated-assets.json": {"assets": [f["path"] for f in registry["files"] if f["deprecated"]]},
        "ownership-map.json": {"version": "1.0.0", "default_owner": "repository-maintainers", "owners": {}},
        "integrity-baseline.json": {"version": "1.0.0", "source": "repository-manifest.json", "integrity": repo["integrity"]},
    }
    mismatches = []
    for name, data in generated.items():
        target = OUT / name
        rendered = json.dumps(data, indent=2, sort_keys=True) + "\n"
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != rendered:
                mismatches.append(name)
        else:
            write_json(target, data)
    if args.check and mismatches:
        print("Manifest drift detected:")
        for name in mismatches:
            print(f" - {name}")
        return 1
    print(json.dumps(repo, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
