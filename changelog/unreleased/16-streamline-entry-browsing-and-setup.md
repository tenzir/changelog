---
title: Streamline entry browsing and setup
type: breaking
authors:
- codex
created: 2025-10-24
---

Promotes `tenzir-changelog show` as the consolidated entry point for browsing changelog entries. The command defaults to the table layout and adds quick transforms—`show -c` for cards, `show -m` for Markdown, and `show -j` for JSON—so reviewers can swap contexts without juggling subcommands. Retires `tenzir-changelog bootstrap` in favor of an automatic setup path: the first `tenzir-changelog add` now creates `config.yaml`, prepares the required directories, and infers the project identifier to streamline onboarding for new repositories.

This is a breaking change for automation and documentation that previously relied on `tenzir-changelog bootstrap`; update any scripts or onboarding guides to drop that command and rely on the new implicit setup flow.

Refines supporting docs and tests to reflect the new command surface and updates defaults so running `tenzir-changelog` without arguments opens the consolidated `show` view.
