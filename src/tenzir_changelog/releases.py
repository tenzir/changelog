"""Release manifest management."""

from __future__ import annotations

from collections.abc import Iterable as IterableCollection
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Optional

import yaml

from .entries import Entry

RELEASE_DIR = Path("releases")


@dataclass
class ReleaseManifest:
    """Representation of a release manifest."""

    version: str
    title: str
    description: str
    project: str
    created: date
    entries: list[str]
    intro: str | None = None
    path: Path | None = None


def release_directory(project_root: Path) -> Path:
    """Return the path containing release manifests."""
    return project_root / RELEASE_DIR


def _parse_frontmatter(path: Path) -> tuple[dict[str, object], str | None]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        data = yaml.safe_load(content) or {}
        return data, None
    _, _, remainder = content.partition("---\n")
    frontmatter, _, body = remainder.partition("\n---\n")
    data = yaml.safe_load(frontmatter) or {}
    intro = body.strip() if body else ""
    return data, intro or None


def _parse_created_date(raw_value: object | None) -> date:
    if raw_value is None:
        return date.today()
    return date.fromisoformat(str(raw_value))


def _normalize_entries_field(raw_value: object | None) -> list[str]:
    if raw_value is None:
        return []
    if isinstance(raw_value, str):
        return [raw_value]
    if isinstance(raw_value, IterableCollection):
        return [str(item) for item in raw_value]
    return [str(raw_value)]


def iter_release_manifests(project_root: Path) -> Iterable[ReleaseManifest]:
    """Yield release manifests from disk."""
    directory = release_directory(project_root)
    if not directory.exists():
        return

    paths = sorted(list(directory.glob("*.md")))
    if not paths:
        paths = sorted(directory.glob("*.yaml"))

    for path in paths:
        data, body_text = _parse_frontmatter(path)

        raw_description = str(data.get("description", "") or "").strip()
        raw_intro = str(data.get("intro", "") or "").strip()
        project_value = data.get("project")
        if not project_value:
            project_value = data.get("product", "")

        description = raw_description
        intro = raw_intro

        body_text = (body_text or "").strip()
        if body_text:
            if not description:
                if "\n\n" in body_text:
                    description_part, remainder = body_text.split("\n\n", 1)
                    description = description_part.strip()
                    remainder = remainder.strip()
                    if not intro:
                        intro = remainder
                    elif remainder:
                        intro = "\n\n".join([intro, remainder]).strip()
                else:
                    description = body_text
            elif not intro:
                intro = body_text

        created_value = _parse_created_date(data.get("created"))
        entries_value = _normalize_entries_field(data.get("entries"))

        manifest = ReleaseManifest(
            version=str(data.get("version") or path.stem),
            title=str(data.get("title", "")),
            description=description,
            project=str(project_value or ""),
            created=created_value,
            entries=entries_value,
            intro=intro,
            path=path,
        )
        yield manifest


def used_entry_ids(project_root: Path) -> set[str]:
    """Return a set containing entry IDs that already belong to a release."""
    used = set()
    for manifest in iter_release_manifests(project_root):
        used.update(manifest.entries)
    return used


def unused_entries(entries: Iterable[Entry], used_ids: set[str]) -> list[Entry]:
    """Filter entries that have not yet been included in a release."""
    return [entry for entry in entries if entry.entry_id not in used_ids]


def _format_frontmatter(data: dict[str, object]) -> str:
    yaml_block = yaml.safe_dump(data, sort_keys=False).strip()
    return f"---\n{yaml_block}\n---\n"


def write_release_manifest(project_root: Path, manifest: ReleaseManifest) -> Path:
    """Serialize and store a release manifest as Markdown with frontmatter."""
    directory = release_directory(project_root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{manifest.version}.md"
    if path.exists():
        raise FileExistsError(f"Release manifest {path} already exists")
    payload: dict[str, object] = {
        "version": manifest.version,
        "title": manifest.title,
        "project": manifest.project,
        "created": manifest.created.isoformat(),
        "entries": list(manifest.entries),
    }
    frontmatter = _format_frontmatter(payload)
    body_parts = []
    if manifest.description:
        body_parts.append(manifest.description.strip())
    if manifest.intro:
        body_parts.append(manifest.intro.strip())
    body = "\n\n".join(part for part in body_parts if part)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(frontmatter)
        if body:
            handle.write("\n" + body + "\n")
    return path


def build_entry_release_index(
    project_root: Path, *, project: Optional[str] = None
) -> dict[str, list[str]]:
    """Return a mapping from entry id to associated release versions."""
    index: dict[str, list[str]] = {}
    for manifest in iter_release_manifests(project_root):
        if project and manifest.project and manifest.project != project:
            continue
        for entry_id in manifest.entries:
            versions = index.setdefault(entry_id, [])
            if manifest.version not in versions:
                versions.append(manifest.version)
    for versions in index.values():
        versions.sort()
    return index
