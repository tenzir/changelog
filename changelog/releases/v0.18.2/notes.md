This release adds persistent configuration support for explicit link formatting, allowing projects to set a default link rendering style in `config.yaml` that applies across all commands.

## 🔧 Changes

### explicit_links configuration option

The `explicit_links` option can now be configured in `config.yaml`, allowing consistent link formatting across all commands that render release notes and changelog entries.

Previously, the `--explicit-links` flag only worked with the `release create` command and had no persistent setting. Now you can set `explicit_links: true` in your project's `config.yaml` to enable explicit Markdown link rendering by default for all commands (`release create`, `release notes`, and `show`). Individual command invocations can still override the config default with `--explicit-links` or `--no-explicit-links` flags.

This ensures consistent output across commands without requiring repeated flag usage, improving the user experience for projects that always want explicit link rendering.

*By @mavam and @claude.*
