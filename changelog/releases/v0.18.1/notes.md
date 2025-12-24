This release adds explicit Markdown link conversion for GitHub references, enabling better compatibility with external documentation sites and Markdown renderers that don't automatically link @mentions and #PR references.

## 🚀 Features

### explicit-links flag for release create command

Add `--explicit-links` flag to the `release create` command to convert GitHub shorthand (@mentions and #PR references) into explicit Markdown links.

This flag enables exporting release notes to documentation sites or other Markdown renderers that don't automatically link GitHub references. To maintain consistency across the CLI, the option is now shared between `release create`, `release notes`, and `show` commands via dedicated option decorators.

The Python API's `Changelog.release_create()` method now accepts an `explicit_links` parameter to support this feature programmatically.

*By @mavam and @claude.*
