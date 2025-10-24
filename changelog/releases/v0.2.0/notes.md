## Features

- Add an optional compact export mode that renders bullet lists with bold titles and first-paragraph excerpts for Markdown and JSON outputs.

## Changes

- Release manifests now keep metadata in `manifest.yaml`, store archived entries in `releases/<version>/entries/`, and write release notes to `notes.md` for consistent automation.
- Entry parsing now converts `created` metadata to real dates and emits them for consumers.
- Drop the workspace section from `config.yaml` in favor of top-level project metadata and update tooling, docs, and samples accordingly.
- Ensure CLI views and exports stay reverse chronological by breaking same-day ties with entry file modification times.
- Tighten the CLI entry table so IDs ellipsize instead of wrapping and adjust column widths to keep titles readable.
- Entry files no longer store the project key; the CLI infers it from config.
- Render entry types with aligned emoji icons, and gate the project banner behind an opt-in `--banner` flag.

## Bug fixes

- When attempting to run `tenzir-changelog` outside a project root, you now get a helpful error message that's properly formatted.
