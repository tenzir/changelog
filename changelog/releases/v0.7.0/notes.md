Expose the CLI as a Python API.

## 🚀 Features

### Expose Python API

The CLI commands are now reusable from Python via the new `tenzir_changelog.Changelog` helper and shared helper functions. You can now drive the same workflows from another script:

```python
from pathlib import Path
from tenzir_changelog import Changelog

client = Changelog(root=Path("changelog"))
client.add(title="API entry", entry_type="feature", description="Body text")
client.show(identifiers=["unreleased"], view="json", include_emoji=False)
```

*By @codex and @mavam.*
