Refine release manifest format: rename 'description' to 'intro' and render it with a folded YAML block for better readability.

## 💥 Breaking changes

### Rename manifest field to intro

Replaced the release manifest field `description` with a single `intro` field. The CLI now accepts `--intro` (instead of `--description`) or `--intro-file` (mutually exclusive) to populate the manifest’s `intro`. The tool no longer writes a `description` key to manifests.

*By @codex.*

## 🚀 Features

### Use folded YAML block for release intro

Release manifests now serialize the `intro` field with a folded block scalar (`>`) for readable multi-line wrapping instead of a single long scalar.

*By @codex and @mavam.*
