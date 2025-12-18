---
title: New `--no-latest` and `--commit` options for release publishing
type: feature
authors:
  - mavam
  - claude
created: 2025-12-18T19:20:52.007445Z
---

The `release publish` command now supports two new options for smoother release
automation:

- `--no-latest` prevents GitHub from marking the release as latest, useful for
  backport releases to older branches
- `--commit` commits staged changes before creating the tag, eliminating a
  manual step in release workflows. The commit message defaults to
  `Release {version}` but can be customized via `--commit-message` or the
  `release.commit_message` config option.
