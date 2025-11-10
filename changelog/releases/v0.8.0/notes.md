Infer GitHub context for entries, keep the Python API non-interactive, and showcase components in the dogfooded project.

## 🚀 Features

### Components in dogfooded project

We now use *components* in the dogfooded project to illustrate the feature.

The first two components are `cli` and `python` to differentiate the primary two usage styles.

*By @mavam.*

### Infer GitHub context for entries

**Component:** `cli`

`tenzir-changelog add` now reads your local `gh` login and the active pull request to auto-populate `authors` and `prs`, so you can skip passing `--author` and `--pr` when the data already exists.

*By @codex and @mavam.*

## 🔧 Changes

### Enforce release version verification

Post-publish CI now checks that the version installed from PyPI matches the release tag, preventing stale artifacts.

*By @codex.*

## 🐞 Bug fixes

### Keep the Python API non-interactive

**Component:** `python`

Using the `Changelog.add()` helper no longer triggers interactive prompts.

Automation that omits authors or entry types now completes without hanging and uses safe defaults instead.

*By @codex and @mavam.*
