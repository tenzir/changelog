This patch release improves the CLI display with better card view styling and author formatting. The card view now displays type-colored borders and properly formats non-GitHub authors without the @ prefix for improved readability.

## 🔧 Changes

### Format non-GitHub authors without @ prefix

**Components:** `cli`

Authors that contain spaces are now displayed without the `@` prefix. Previously, all authors were rendered with `@` regardless of format, which produced awkward output like `@Jane Smith` for non-GitHub users. Now only GitHub-style handles (single words without spaces) receive the `@` prefix.

*By @mavam and @claude.*

### Improve card view styling

**Components:** `cli`

Card view now displays type-colored borders (orange for breaking, red for bugfix, green for feature, blue for change) and uses the plural "Components" label.

*By @mavam and @claude.*
