#!/usr/bin/env python3
"""Static integrity audit for the Logistics Knowledge Base.

Checks local file references, Python local imports, JSON $refs, event vocabulary,
entity vocabulary, and event-schema coverage. It is intentionally stdlib-only so
it can run before application dependencies are installed.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}
LOCAL_EXTENSIONS = {".json", ".jsonld", ".geojson", ".md", ".mmd", ".py", ".html", ".xml", ".txt"}


def files():
    return [p for p in ROOT.rglob("*") if p.is_file() and not any(part in IGNORED_DIRS for part in p.parts)]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def walk_strings(value):
    if isinstance(value, dict):
        for v in value.values():
            yield from walk_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_strings(v)
    elif isinstance(value, str):
        yield value


def resolve_local(raw: str, source: Path):
    if raw.startswith(("http://", "https://", "urn:", "kg:", "schema:")):
        return None
    candidate = raw.split("#", 1)[0].strip().lstrip("./")
    if not candidate or "://" in candidate:
        return None
    if candidate.startswith("/"):
        return ROOT / candidate.lstrip("/")
    return source.parent / candidate


def check_json_refs(all_paths, errors):
    for path in all_paths:
        if path.suffix not in {".json", ".jsonld"}:
            continue
        try:
            data = load_json(path)
        except Exception as exc:
            errors.append(f"INVALID_JSON {path.relative_to(ROOT)}: {exc}")
            continue
        for value in walk_strings(data):
            if "$ref" in value or value.startswith("/") or any(value.endswith(ext) for ext in LOCAL_EXTENSIONS):
                target = resolve_local(value, path)
                if target and target.suffix in LOCAL_EXTENSIONS and not target.exists():
                    # Try repository-root-relative paths as a second interpretation.
                    root_target = ROOT / value.lstrip("/")
                    if not root_target.exists():
                        errors.append(f"MISSING_REF {path.relative_to(ROOT)} -> {value}")


def check_markdown_refs(all_paths, errors):
    pattern = re.compile(r"(?:\]\(|\b(?:file|path|source|schema|registry|root|workflow|script)\s*[:=]\s*)([^)\s]+)")
    for path in all_paths:
        if path.suffix not in {".md", ".mmd", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in pattern.finditer(text):
            raw = match.group(1).strip('`\"\'<>')
            target = resolve_local(raw, path)
            if target and target.suffix in LOCAL_EXTENSIONS and not target.exists():
                root_target = ROOT / raw.lstrip("/")
                if not root_target.exists():
                    errors.append(f"MISSING_TEXT_REF {path.relative_to(ROOT)} -> {raw}")


def local_python_modules(all_paths):
    modules = set()
    for path in all_paths:
        if path.suffix == ".py":
            modules.add(path.stem)
    return modules


def check_python_imports(all_paths, errors):
    modules = local_python_modules(all_paths)
    for path in all_paths:
        if path.suffix != ".py":
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"INVALID_PYTHON {path.relative_to(ROOT)}: {exc}")
            continue
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module.split(".")[0]]
            for name in names:
                if name in modules:
                    # A same-directory module is valid when the script is executed directly;
                    # package-qualified imports are handled by Python's normal path rules.
                    continue
                if name in {"api", "graph", "processors", "ai", "ai_agent"}:
                    package_dir = ROOT / name.replace("_", "-")
                    if not package_dir.exists():
                        errors.append(f"MISSING_LOCAL_PACKAGE {path.relative_to(ROOT)} -> {name}")


def event_protocol_sets():
    protocol = load_json(ROOT / "protocol" / "logistics-event-protocol-v1.json")
    events = {event for category in protocol["eventCategories"] for event in category["events"]}
    entities = set(protocol["supportedEntities"])
    return events, entities


def schema_event_type(schema):
    direct = schema.get("eventType")
    if isinstance(direct, str):
        return direct
    for branch in schema.get("allOf", []):
        const = branch.get("properties", {}).get("eventType", {}).get("const")
        if isinstance(const, str):
            return const
    return None


def check_event_integrity(all_paths, errors):
    protocol_events, protocol_entities = event_protocol_sets()
    schema_events = {}
    for path in all_paths:
        if path.parent.name != "events" or path.name == "logistics-event.schema.json" or path.suffix != ".json":
            continue
        try:
            event_type = schema_event_type(load_json(path))
        except Exception:
            continue
        if event_type:
            schema_events[event_type] = path
            if event_type not in protocol_events:
                errors.append(f"EVENT_NOT_IN_PROTOCOL {path.relative_to(ROOT)} -> {event_type}")

    for event_type, path in sorted(schema_events.items()):
        if not path.exists():
            errors.append(f"EVENT_SCHEMA_MISSING {event_type}")

    envelope = load_json(ROOT / "events" / "logistics-event.schema.json")
    entity_enum = set(envelope["properties"]["entityType"]["enum"])
    if entity_enum != protocol_entities:
        missing = sorted(protocol_entities - entity_enum)
        extra = sorted(entity_enum - protocol_entities)
        errors.append(f"ENTITY_VOCABULARY_MISMATCH missing={missing} extra={extra}")


def main():
    errors = []
    all_paths = files()
    check_json_refs(all_paths, errors)
    check_markdown_refs(all_paths, errors)
    check_python_imports(all_paths, errors)
    check_event_integrity(all_paths, errors)

    print(f"Repository files scanned: {len(all_paths)}")
    print(f"Integrity findings: {len(errors)}")
    for error in errors:
        print(f"- {error}")

    # The audit is currently advisory because legacy documentation contains some
    # intentionally illustrative references. CI can promote individual classes to
    # hard failures as the repository converges.
    return 0


if __name__ == "__main__":
    sys.exit(main())
