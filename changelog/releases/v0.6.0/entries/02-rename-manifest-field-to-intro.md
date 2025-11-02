---
title: Rename manifest field to intro
type: breaking
authors:
- codex
created: 2025-11-02
---

Replaced the release manifest field `description` with a single `intro` field. The CLI now accepts `--intro` (instead of `--description`) or `--intro-file` (mutually exclusive) to populate the manifest’s `intro`. The tool no longer writes a `description` key to manifests.
