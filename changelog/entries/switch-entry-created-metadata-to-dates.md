---
title: Store entry creation dates as Date objects
type: change
authors:
- codex
created: 2025-10-21
---

Entry parsing now converts `created` metadata to real `datetime.date` objects and
persists them when writing entries, ensuring downstream consumers receive typed
values instead of plain strings.
