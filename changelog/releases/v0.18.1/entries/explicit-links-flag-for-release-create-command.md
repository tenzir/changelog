---
title: explicit-links flag for release create command
type: feature
authors:
  - mavam
  - claude
created: 2025-12-24T07:10:35.83934Z
---

Add `--explicit-links` flag to the `release create` command to convert GitHub shorthand (@mentions and #PR references) into explicit Markdown links.

This flag enables exporting release notes to documentation sites or other Markdown renderers that don't automatically link GitHub references. To maintain consistency across the CLI, the option is now shared between `release create`, `release notes`, and `show` commands via dedicated option decorators.

The Python API's `Changelog.release_create()` method now accepts an `explicit_links` parameter to support this feature programmatically.
