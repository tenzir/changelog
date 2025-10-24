---
title: Support tagging during release publish
type: feature
authors:
- codex
created: 2025-10-24
---

Add a `--tag` flag to `release publish` so the command can create the annotated Git tag before invoking the GitHub workflow, logging a warning and skipping creation when the tag already exists.
