"""Entry management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Optional

import yaml

from .utils import slugify

ENTRY_DIR = Path("entries")
ENTRY_TYPES = ("feature", "bugfix", "change")


@dataclass
class Entry:
    """Representation of a changelog entry file."""

    entry_id: str
    metadata: dict[str, Any]
    body: str
    path: Path

    @property
    def title(self) -> str:
        return str(self.metadata.get("title", "Untitled"))

    @property
    def type(self) -> str:
        return str(self.metadata.get("type", "change"))

    @property
    def project(self) -> Optional[str]:
        """Return the single project an entry belongs to."""
        try:
            return normalize_project(self.metadata)
        except ValueError as exc:
            raise ValueError(
                f"Entry '{self.entry_id}' has invalid project metadata: {exc}"
            ) from exc

    @property
    def projects(self) -> list[str]:
        project = self.project
        return [project] if project else []

    @property
    def products(self) -> list[str]:  # backwards compatibility
        return self.projects

    @property
    def created_at(self) -> Optional[date]:
        created = self.metadata.get("created")
        if not created:
            return None
        try:
            return date.fromisoformat(str(created))
        except ValueError:
            return None


def entry_directory(project_root: Path) -> Path:
    """Return the entries directory inside the project."""
    return project_root / ENTRY_DIR


def read_entry(path: Path) -> Entry:
    """Parse a markdown entry file with YAML frontmatter."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise ValueError(f"Entry {path} missing YAML frontmatter")

    _, _, remainder = content.partition("---\n")
    frontmatter, _, body = remainder.partition("\n---\n")
    metadata = yaml.safe_load(frontmatter) or {}
    entry_id = path.stem
    return Entry(entry_id=entry_id, metadata=metadata, body=body.strip(), path=path)


def iter_entries(project_root: Path) -> Iterable[Entry]:
    """Yield changelog entries from disk."""
    directory = entry_directory(project_root)
    if not directory.exists():
        return
    for path in sorted(directory.glob("*.md")):
        yield read_entry(path)


def generate_entry_id(seed: Optional[str] = None) -> str:
    """Generate a deterministic-ish entry id based on optional seed."""
    if seed:
        slug = slugify(seed)
        if slug:
            return slug[:80]
    import secrets

    return secrets.token_hex(6)


def _coerce_project(value: Any, *, source: str) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, (list, tuple, set)):
        normalized = [str(item).strip() for item in value if str(item).strip()]
        if not normalized:
            return None
        if len(normalized) > 1:
            raise ValueError(
                f"{source} must contain a single project, got: {', '.join(normalized)}"
            )
        return normalized[0]
    return str(value).strip() or None


def normalize_project(
    metadata: dict[str, Any],
    default: Optional[str] = None,
) -> Optional[str]:
    """Normalize project metadata to the singular `project` key."""
    project = _coerce_project(metadata.get("project"), source="project")
    legacy_keys = ("projects", "products")

    if project is None:
        for key in legacy_keys:
            if key in metadata:
                project = _coerce_project(metadata.get(key), source=key)
            metadata.pop(key, None)
            if project is not None:
                break
        if project is None and default is not None:
            project = default
    else:
        for key in legacy_keys:
            metadata.pop(key, None)

    if project is None:
        metadata.pop("project", None)
        return None

    metadata["project"] = project
    return project


def format_frontmatter(metadata: dict[str, Any]) -> str:
    """Render metadata as YAML frontmatter for an entry file."""
    cleaned: dict[str, Any] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        cleaned[key] = value
    yaml_block = yaml.safe_dump(cleaned, sort_keys=False).strip()
    return f"---\n{yaml_block}\n---\n"


def write_entry(
    project_root: Path,
    metadata: dict[str, Any],
    body: str,
    entry_id: Optional[str] = None,
    *,
    default_project: Optional[str] = None,
) -> Path:
    """Write a new entry file and return its path."""
    directory = entry_directory(project_root)
    directory.mkdir(parents=True, exist_ok=True)
    entry_type = str(metadata.get("type", "change"))
    if entry_type not in ENTRY_TYPES:
        raise ValueError(
            f"Unknown entry type '{entry_type}'. Expected one of: {', '.join(ENTRY_TYPES)}"
        )
    metadata["type"] = entry_type
    project_value = normalize_project(metadata, default=default_project)
    if default_project is not None and project_value == default_project:
        metadata.pop("project", None)
    entry_id = entry_id or generate_entry_id(metadata.get("title"))
    path = directory / f"{entry_id}.md"

    if path.exists():
        base = entry_id
        counter = 1
        while True:
            candidate = f"{base}-{counter}"
            candidate_path = directory / f"{candidate}.md"
            if not candidate_path.exists():
                entry_id = candidate
                path = candidate_path
                break
            counter += 1

    metadata.setdefault("created", date.today().isoformat())
    frontmatter = format_frontmatter(metadata)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(frontmatter)
        if body:
            handle.write("\n" + body.strip() + "\n")
    return path
