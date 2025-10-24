"""Quality gate runner for tenzir-changelog."""

from __future__ import annotations

import shlex
import subprocess
from typing import Sequence

from .utils import configure_logging, log_info

_COMMANDS: Sequence[Sequence[str]] = (
    ("ruff", "format", "--check"),
    ("ruff", "check"),
    ("mypy",),
    ("pytest",),
    ("uv", "build"),
)


def _run(command: Sequence[str]) -> None:
    printable = " ".join(shlex.quote(part) for part in command)
    log_info(f"running {printable}")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    configure_logging(debug=False)
    for command in _COMMANDS:
        _run(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
