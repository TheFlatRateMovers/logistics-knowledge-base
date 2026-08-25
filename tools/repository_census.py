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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_tracked() -> set[str]:
    try:
        result = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True)
        return {line for line in result.stdout.splitlines() if line}
    except (OSError, subprocess.CalledProcessError):
        return set()


def classify(path: Path) -> str:
    p = rel(path).lower()
    if p.startswith("repository-manifest/"):
        return "generated"
    if p.startswith("tools/") or p.startswith(".github/workflows/"):
        return "runtime"
    if any(token in p for token in ("deprecated", "archive", "legacy")):
        return "deprecated"
    if any(token in p for token in ("generated", "build", "dist", "output", "vector-index")):
        return "generated"
    if p.startswith(("docs/", "documentation/")) or path.suffix.lower() in {".md", ".markdown"}:
        return "documentation"
    if any(token in p for token in ("experiment", "prototype", "sandbox")):
        return "experimental"
    if any(token in p for token in ("ontology/", "datasets/", "schemas/", "protocols/", "glossaries/", "geojson/", "case-studies/", "faq/", "compliance/", "equipment/", "infrastructure/")):
        return "canonical"
    return "unknown"


def purpose(path: Path) -> str:
    p = rel(path)
    ext = path.suffix.lower()
    if p == "README.md":
        return "Repository entry documentation"
    if p.startswith("tools/"):
        return "Repository engineering automation"
    if p.startswith("repository-manifest/"):
        return "Repository stabilization metadata"
    if p.startswith(".github/workflows/"):
        return "Continuous integration workflow"
    if ext in {".json", ".jsonld", ".yaml", ".yml"}:
        return "Structured data or configuration"
    if ext in {".py", ".js", ".ts", ".tsx", ".jsx"}:
        return "Executable source code"
    if ext in {".md", ".markdown", ".txt"}:
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
    patterns = [
        r"(?:\]\(|\"|')((?:\.\.?/|/)?[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+)",
        r"\$ref\s*:\s*['\"]([^'\"]+)['\"]",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, text):
            candidate = match.split("#", 1)[0].strip()
            if candidate and not candidate.startswith(("http://", "https://")):
                refs.add(candidate)
    return sorted(refs)


def resolve_reference(source: str, target: str, all_paths: set[str]) -> str | None:
    if target.startswith("#"):
        return None
    candidate = (Path(source).parent / target).as_posix()
    candidate = candidate.lstrip("./")
    options = [candidate, f"{candidate}.md", f"{candidate}.json", f"{candidate}.jsonld", f"{candidate}.py"]
    for option in options:
        if option in all_paths:
            return option
    return None


def census() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    tracked = git_tracked()
    paths = [
        path for path in sorted(ROOT.rglob("*"))
        if path.is_file() and not any(part in IGNORE_DIRS for part in path.parts)
    ]
    all_paths = {rel(path) for path in paths}
    files: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []
    extension_counts: dict[str, int] = defaultdict(int)
    status_counts: dict[str, int] = defaultdict(int)

    for path in paths:
        rp = rel(path)
        status = classify(path)
        ext = path.suffix.lower() or "[no extension]"
        extension_counts[ext] += 1
        status_counts[status] += 1
        refs = text_references(path)
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
            "references": refs,
        }
        if path.suffix.lower() == ".py":
            record["python_imports"] = python_imports(path)
        files.append(record)
        for target in refs:
            resolved = resolve_reference(rp, target, all_paths)
            if resolved:
                edges.append({"source": rp, "target": resolved, "kind": "local-reference"})
            else:
                missing.append({"source": rp, "reference": target})

    duplicate_hashes: dict[str, list[str]] = defaultdict(list)
    duplicate_names: dict[str, list[str]] = defaultdict(list)
    for record in files:
        duplicate_hashes[record["sha256"]].append(record["path"])
        duplicate_names[record["name"]].append(record["path"])
    duplicate_hashes = {key: value for key, value in duplicate_hashes.items() if len(value) > 1}
    duplicate_names = {key: value for key, value in duplicate_names.items() if len(value) > 1}

    repository = {
        "manifest_version": "1.0.0",
        "repository": "TheFlatRateMovers/logistics-knowledge-base",
        "generated_by": "tools/repository_census.py",
        "tracked_file_count": len(tracked),
        "scanned_file_count": len(files),
        "extension_inventory": dict(sorted(extension_counts.items())),
        "status_inventory": dict(sorted(status_counts.items())),
        "integrity": {
            "missing_local_references": len(missing),
            "duplicate_content_groups": len(duplicate_hashes),
            "duplicate_filename_groups": len(duplicate_names),
        },
    }
    registry = {"manifest_version": "1.0.0", "files": files}
    dependencies = {"manifest_version": "1.0.0", "edges": edges, "missing_references": missing}
    return repository, registry, dependencies


def render(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when committed manifest output is stale")
    args = parser.parse_args()
    repository, registry, dependencies = census()
    generated = {
        "repository-manifest.json": repository,
        "file-registry.json": registry,
        "dependency-registry.json": dependencies,
        "canonical-assets.json": {"assets": [f["path"] for f in registry["files"] if f["canonical"]]},
        "generated-assets.json": {"assets": [f["path"] for f in registry["files"] if f["generated"]]},
        "runtime-assets.json": {"assets": [f["path"] for f in registry["files"] if f["runtime"]]},
        "deprecated-assets.json": {"assets": [f["path"] for f in registry["files"] if f["deprecated"]]},
        "ownership-map.json": {"version": "1.0.0", "default_owner": "repository-maintainers", "owners": {}},
        "integrity-baseline.json": {"version": "1.0.0", "source": "repository-manifest.json", "integrity": repository["integrity"]},
    }
    mismatches: list[str] = []
    for name, data in generated.items():
        target = OUT / name
        output = render(data)
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != output:
                mismatches.append(name)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
    if mismatches:
        print("Manifest drift detected:")
        print("\n".join(f" - {name}" for name in mismatches))
        return 1
    print(render(repository))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
