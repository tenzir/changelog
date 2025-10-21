# Development Guide

This document outlines day-to-day workflows for contributors to
`tenzir-changelog`. You need Python 3.12+ and
[uv](https://docs.astral.sh/uv/) to get started.

## Setup

Install dependencies into the managed virtual environment:

```sh
uv sync --python 3.12
```

This creates `.venv/` containing runtime dependencies and the local tooling
stack.

## Using the Project Interpreter

Run commands inside the managed environment with `uv run`. For an interactive
shell:

```sh
uv run python
```

## Common Tasks

- Format & lint:
  ```sh
  uv run ruff format
  uv run ruff check
  ```
- Run the test suite:
  ```sh
  uv run pytest
  ```
- Type-check:
  ```sh
  uv run mypy
  ```
- Build distributions:
  ```sh
  uv build
  ```

- Aggregate quality gate:
  ```sh
  uv run check-release
  ```

## Quality Gates

Before opening a pull request, ensure the combined workflow passes:

```sh
uv run check-release
```

The helper sequentially runs the formatter (diff-only), lint, type checks, the
test suite, and a distribution build. To run steps individually:

```sh
uv run ruff format --check
uv run ruff check
uv run mypy
uv run pytest
uv build
```

## Releasing

Releases use trusted publishing from GitHub Actions. When ready:

1. Confirm the tree is clean and checks pass:
   ```sh
   uv run check-release
   ```
2. Bump the version:
   ```sh
   uv version --bump <part>
   ```
3. Commit changes:
   ```sh
   git commit -am "Bump version to vX.Y.Z"
   ```
4. Tag and push:
   ```sh
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push && git push --tags
   ```
5. Draft and publish a GitHub release describing highlights.

Publishing the release triggers the automated workflow that builds, validates,
and uploads artifacts to PyPI before smoke-testing the package.

## Pull Requests

- Keep changes focused and reference related issues when possible.
- Update documentation and examples when behavior changes.
- Ensure continuous integration is green before requesting review.
