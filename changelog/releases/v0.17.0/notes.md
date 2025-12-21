This release enhances shell scripting capabilities by making `release create`
output the version to stdout. All Rich UI elements now go to stderr, enabling
clean machine-readable results for automation workflows.

## 🚀 Features

### Machine-readable version output from release create

The `release create` command now outputs the created version to stdout, enabling
shell scripting patterns like `VERSION=$(tenzir-changelog release create --minor --yes)`.
All Rich output (tables, panels) now goes to stderr, keeping stdout clean for
machine-readable results.

_By @mavam and @claude._
