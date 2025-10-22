---
title: Show individual changelog entries
type: feature
authors:
- mavam
- codex
created: 2025-10-22
---

Display detailed information for a single changelog entry using the new `--entry` flag.

The `show` command now accepts an `--entry` option that displays a specific changelog entry with:
- Metadata (entry ID, type, creation date, authors, PRs)
- Release status (unreleased or which versions it appears in)
- Formatted markdown body with syntax highlighting

The flag supports partial matching, so you can use shortened entry IDs:

```sh
# Full entry ID
tenzir-changelog show --entry configure-export-style-defaults

# Partial match (matches unique substring)
tenzir-changelog show --entry configure
```

This makes it easy to review individual entries before releasing or to reference
specific changes.
