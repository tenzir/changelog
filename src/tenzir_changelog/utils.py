"""Shared utilities for the CLI implementation."""

from __future__ import annotations

import logging
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from rich.console import Console, RenderableType
from rich.style import Style
from rich.theme import Theme

CHECKMARK = "\033[92;1m✔\033[0m"
CROSS = "\033[31m✘\033[0m"
INFO = "\033[94;1mi\033[0m"
DEBUG_PREFIX = "\033[95m◆\033[0m"

CHECKMARK_PREFIX = f"{CHECKMARK} "
CROSS_PREFIX = f"{CROSS} "
INFO_PREFIX = f"{INFO} "
DEBUG_PREFIX_WITH_SPACE = f"{DEBUG_PREFIX} "

_LOGGER_NAME = "tenzir_changelog"
_LOGGER = logging.getLogger(_LOGGER_NAME)

console = Console(
    theme=Theme(
        {
            "markdown.code": Style(bold=True, color="cyan"),
            "markdown.code_block": Style(color="cyan"),
        }
    )
)


def configure_logging(debug: bool = False) -> logging.Logger:
    """Configure the shared logger used across the CLI."""
    level = logging.DEBUG if debug else logging.INFO
    _LOGGER.setLevel(level)
    while _LOGGER.handlers:
        handler = _LOGGER.handlers.pop()
        handler.close()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.setLevel(level)
    _LOGGER.addHandler(handler)
    _LOGGER.propagate = False
    return _LOGGER


def _log(prefix: str, message: str, level: int) -> None:
    logger = logging.getLogger(_LOGGER_NAME)
    lines = message.splitlines() or [""]
    for line in lines:
        if line:
            logger.log(level, f"{prefix}{line}")
        else:
            logger.log(level, prefix.rstrip())


def log_info(message: str) -> None:
    """Log an informational message with the standardized prefix."""
    _log(INFO_PREFIX, message, logging.INFO)


def log_success(message: str) -> None:
    """Log a success message with the standardized prefix."""
    _log(CHECKMARK_PREFIX, message, logging.INFO)


def log_error(message: str) -> None:
    """Log an error message with the standardized prefix."""
    _log(CROSS_PREFIX, message, logging.ERROR)


def log_debug(message: str) -> None:
    """Log a debug message with the standardized prefix."""
    _log(DEBUG_PREFIX_WITH_SPACE, message, logging.DEBUG)


def render_to_text(renderable: RenderableType) -> str:
    """Return the string representation of a Rich renderable."""
    with console.capture() as capture:
        console.print(renderable)
    return capture.get()


def emit_output(content: str, *, newline: bool = True) -> None:
    """Emit raw command output through the shared logger without prefixes."""
    logger = logging.getLogger(_LOGGER_NAME)
    handler_terminators: list[tuple[logging.Handler, str]] = []
    if not newline:
        for handler in logger.handlers:
            if hasattr(handler, "terminator"):
                handler_terminators.append((handler, getattr(handler, "terminator")))
                setattr(handler, "terminator", "")
    try:
        logger.log(logging.INFO, content)
    finally:
        for handler, terminator in handler_terminators:
            setattr(handler, "terminator", terminator)


def coerce_date(value: object) -> Optional[date]:
    """Return a date object for ISO-like inputs, preserving None."""
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value).strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


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


def extract_excerpt(text: str) -> str:
    """Return the first paragraph of a Markdown body as a single line."""
    stripped = text.strip()
    if not stripped:
        return ""
    first_paragraph, *_ = re.split(r"\n\s*\n", stripped, maxsplit=1)
    collapsed = re.sub(r"\s*\n\s*", " ", first_paragraph.strip())
    return collapsed.strip()
