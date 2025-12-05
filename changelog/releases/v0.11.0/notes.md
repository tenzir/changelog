This release adds the `--co-author` option for crediting additional authors (useful for AI-assisted development) and improves entry parsing to accept the plural `components` key in frontmatter.

## 🚀 Features

### Add --co-author option to add command

The new `--co-author` option allows adding additional authors while preserving automatic author inference. This is useful for AI-assisted development where both the human and coding agent should be credited.

*By @mavam and @claude.*

### Support plural components key in entry frontmatter

**Components:** `cli`, `python`

Entries now support both `component` (singular) and `components` (plural) keys in YAML frontmatter, following the existing patterns for `author`/`authors` and `pr`/`prs`. This allows entries to have multiple components. The CLI `--component` option can be repeated for multiple values.

*By @mavam.*
