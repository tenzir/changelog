---
title: Remove redundant version field from JSON entry objects
type: bugfix
authors:
  - mavam
  - claude
created: 2025-12-19T07:00:23.399539Z
---

The JSON output of `release notes --json` previously included a redundant `version` field in each entry object. Since all entries in a release share the same version as the top-level manifest version, this duplication was unnecessary. The `version` field has been removed from individual entries, with the version information now available only at the top level of the JSON payload.
