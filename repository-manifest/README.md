# Repository Manifest

The Repository Manifest is the machine-readable control plane for repository stabilization.

## Purpose

This directory records the authoritative inventory and integrity baseline of the repository. Generated registry files describe the working tree at census time; they are not intended to replace authored source data.

## Lifecycle

1. `tools/repository_census.py` scans the checkout.
2. Registry JSON files are regenerated from the current tree.
3. CI validates syntax and local references.
4. Changes to canonical, generated, runtime, or deprecated classifications are reviewed as engineering decisions.

## Commands

```bash
python tools/repository_census.py
python tools/repository_census.py --check
```

`--check` returns non-zero when generated registry output differs from the committed baseline.

## Status vocabulary

- `canonical`: authoritative authored source
- `generated`: reproducible derived artifact
- `runtime`: executable/runtime asset
- `documentation`: human-facing documentation
- `experimental`: explicitly non-production work
- `deprecated`: retained for historical compatibility
- `unknown`: not yet classified

The initial census deliberately favors evidence over assumptions. Unknown classifications are findings for later review, not silently promoted to canonical status.
