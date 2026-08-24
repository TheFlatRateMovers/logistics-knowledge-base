# Machine Index Authority

## Canonical entry point

The canonical machine-discovery root for this repository is:

`repository-index/root-pointer.json`

## Discovery precedence

1. `repository-index/root-pointer.json` — canonical root pointer.
2. `repository-index/machine-indexing.registry.jsonld` — canonical machine registry.
3. `ai-crawler-entry/api-manifest.json` — crawler/API capabilities.
4. `ai-crawler-entry/dataset-entry-manifest.json` — dataset discovery.
5. `llms.txt` — human/LLM-oriented top-level discovery.

Versioned artifacts such as `root-pointer.v2.json` and `machine-indexing.registry.v2.jsonld` are retained as historical/versioned artifacts until explicitly promoted. They must not supersede the canonical files implicitly.

## Integrity rule

Any new machine-indexing artifact MUST either:

- be referenced by the canonical root pointer or registry, or
- be explicitly marked experimental/legacy.

This prevents competing discovery roots from silently becoming authoritative.
