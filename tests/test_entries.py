"""Tests for entry helper utilities."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from tenzir_changelog.entries import iter_entries, sort_entries_desc, write_entry


def test_sort_entries_desc_orders_within_same_day(tmp_path: Path) -> None:
    metadata_a = {"title": "Entry A", "type": "change", "created": date(2025, 1, 1)}
    metadata_b = {"title": "Entry B", "type": "change", "created": date(2025, 1, 1)}

    path_a = write_entry(tmp_path, dict(metadata_a), "First body")
    path_b = write_entry(tmp_path, dict(metadata_b), "Second body")

    os.utime(path_a, (1_000_000, 1_000_000))
    os.utime(path_b, (2_000_000, 2_000_000))

    entries = list(iter_entries(tmp_path))
    ordered = sort_entries_desc(entries)

    assert [entry.entry_id for entry in ordered] == [path_b.stem, path_a.stem]
