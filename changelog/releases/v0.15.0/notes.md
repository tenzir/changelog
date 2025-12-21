This release adds new options to the `release publish` command for more flexible release automation. You can now prevent GitHub from marking a release as latest with `--no-latest` (useful for backport releases), and automatically commit staged changes before tagging with `--commit`.

## 🚀 Features

### New `--no-latest` and `--commit` options for release publishing

The `release publish` command now supports two new options for smoother release automation:

- `--no-latest` prevents GitHub from marking the release as latest, useful for backport releases to older branches
- `--commit` commits staged changes before creating the tag, eliminating a manual step in release workflows. The commit message defaults to `Release {version}` but can be customized via `--commit-message` or the `release.commit_message` config option.

_By @mavam and @claude._
