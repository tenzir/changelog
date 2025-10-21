"""Configuration helpers for tenzir-changelog."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

CONFIG_RELATIVE_PATH = Path("config.yaml")


def default_config_path(project_root: Path) -> Path:
    """Return the default config path for a project root."""
    return project_root / CONFIG_RELATIVE_PATH


@dataclass
class WorkspaceSettings:
    """High-level project metadata."""

    name: str
    description: str = ""
    repository: str | None = None


@dataclass
class Config:
    """Structured representation of the changelog config."""

    workspace: WorkspaceSettings
    project: str
    intro_template: str | None = None
    assets_dir: str | None = None


def load_config(path: Path) -> Config:
    """Load the configuration from disk."""
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    workspace_raw = raw.get("workspace")
    if workspace_raw is None or not isinstance(workspace_raw, Mapping):
        maybe_project_obj = raw.get("project")
        if isinstance(maybe_project_obj, Mapping):
            workspace_raw = maybe_project_obj
        else:
            workspace_raw = {}
    workspace = WorkspaceSettings(
        name=str(workspace_raw.get("name", "Unnamed Project")),
        description=str(workspace_raw.get("description", "")),
        repository=(str(workspace_raw["repository"]) if "repository" in workspace_raw else None),
    )

    project_value_raw = raw.get("project")
    if isinstance(project_value_raw, str):
        project_value = project_value_raw.strip()
    else:
        project_value = str(raw.get("project_name", raw.get("product", "")) or "").strip()
    if not project_value:
        raise ValueError("Config missing 'project'")

    return Config(
        workspace=workspace,
        project=project_value,
        intro_template=(str(raw["intro_template"]) if raw.get("intro_template") else None),
        assets_dir=str(raw["assets_dir"]) if raw.get("assets_dir") else None,
    )


def dump_config(config: Config) -> dict[str, Any]:
    """Convert a Config into a plain dictionary suitable for YAML output."""
    project_payload: dict[str, Any] = {
        "name": config.workspace.name,
    }
    if config.workspace.description:
        project_payload["description"] = config.workspace.description
    if config.workspace.repository:
        project_payload["repository"] = config.workspace.repository

    data: dict[str, Any] = {
        "workspace": project_payload,
        "project": config.project,
    }
    if config.intro_template:
        data["intro_template"] = config.intro_template
    if config.assets_dir:
        data["assets_dir"] = config.assets_dir
    return data


def save_config(config: Config, path: Path) -> None:
    """Write the configuration to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(dump_config(config), handle, sort_keys=False)
