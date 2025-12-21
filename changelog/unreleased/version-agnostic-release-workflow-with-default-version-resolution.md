---
title: Version-agnostic release workflow with default version resolution
type: feature
authors:
  - mavam
  - claude
created: 2025-12-21T10:47:35.9378Z
---

The `release publish` command now accepts the version as an optional argument, defaulting to the latest released version when omitted. This makes it easier to publish the most recent release without explicitly specifying its version.

A new `release version` command prints the latest released version. The `--bare` flag strips the `v` prefix, making it convenient for version-agnostic workflows that need to reference the release version in scripts or CI/CD pipelines.

Additionally, release version validation has been strengthened to ensure semantic versioning compliance.
