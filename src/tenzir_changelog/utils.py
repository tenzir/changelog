"""Shared utilities for the CLI implementation."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


def guess_git_remote(project_root: Path) -> Optional[str]:
    """Return the GitHub repository slug (owner/name) if available."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(project_root),
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    url = result.stdout.strip()
    if not url:
        return None
    url = url.replace(".git", "")
    if url.startswith("git@"):
        _, _, remainder = url.partition(":")
        return remainder
    if url.startswith("https://"):
        remainder = url[len("https://") :]
        # Remove domain
        parts = remainder.split("/", 1)
        if len(parts) == 2:
            return parts[1]
    return url


def slugify(value: str) -> str:
    """Generate a safe slug for filesystem or identifier usage."""
    safe_chars = []
    for char in value.lower():
        if char.isalnum():
            safe_chars.append(char)
        elif char in {" ", "-", "_"}:
            safe_chars.append("-")
    slug = "".join(safe_chars)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "project"
