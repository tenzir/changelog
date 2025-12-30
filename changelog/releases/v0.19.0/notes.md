This release adds configuration options to disable automatic PR and author detection, giving projects more control over changelog entry metadata.

## 🚀 Features

### Disable automatic PR and author detection

Add `omit_pr` and `omit_author` configuration options to prevent automatic inference of PR numbers and authors. When these config options are set to `true`, the `add` command will not auto-detect PR numbers from git branches or infer authors from git commits. If users explicitly provide `--pr` or `--author` flags while the corresponding omit option is enabled, a warning message is emitted and the value is ignored. This gives projects fine-grained control over changelog entry metadata.

*By @mavam and @claude.*
