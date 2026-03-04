#!/usr/bin/env python3
"""Ensure TreeDataGrid Lunet docs are available locally."""

from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys

REQUIRED_MARKERS = (
    "site/config.scriban",
    "site/articles/readme.md",
    "src/Avalonia.Controls.TreeDataGrid/Avalonia.Controls.TreeDataGrid.csproj",
)

PREFERRED_API_JSON = (
    "src/Avalonia.Controls.TreeDataGrid/obj/Release/net8.0/"
    "Avalonia.Controls.TreeDataGrid.api.json"
)


def _normalize_docs_root(path: pathlib.Path) -> pathlib.Path:
    resolved = path.expanduser().resolve()

    if (resolved / "site" / "config.scriban").exists():
        return resolved

    if (resolved / "config.scriban").exists() and (resolved / "articles").is_dir():
        return resolved.parent

    if resolved.name == "site" and (resolved / "config.scriban").exists():
        return resolved.parent

    return resolved


def _missing_markers(docs_root: pathlib.Path) -> list[str]:
    return [marker for marker in REQUIRED_MARKERS if not (docs_root / marker).exists()]


def _is_valid_docs_root(docs_root: pathlib.Path) -> bool:
    return not _missing_markers(docs_root)


def _find_api_json(
    docs_root: pathlib.Path,
    explicit_api_json: str | None,
) -> pathlib.Path:
    if explicit_api_json:
        return pathlib.Path(explicit_api_json).expanduser().resolve()

    preferred = docs_root / PREFERRED_API_JSON
    if preferred.exists():
        return preferred

    release_dir = docs_root / "src" / "Avalonia.Controls.TreeDataGrid" / "obj" / "Release"
    candidates = list(release_dir.glob("*/Avalonia.Controls.TreeDataGrid.api.json"))
    candidates.sort(
        key=lambda path: (path.stat().st_mtime if path.exists() else 0, str(path)),
        reverse=True,
    )

    if candidates:
        return candidates[0]

    return preferred


def _candidate_roots() -> list[pathlib.Path]:
    candidates: list[pathlib.Path] = []

    env_docs_root = os.environ.get("TREE_DATAGRID_DOCS_ROOT")
    if env_docs_root:
        candidates.append(pathlib.Path(env_docs_root))

    cwd = pathlib.Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = pathlib.Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    unique: list[pathlib.Path] = []
    seen: set[pathlib.Path] = set()
    for candidate in candidates:
        normalized = _normalize_docs_root(candidate)
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(normalized)

    return unique


def _find_docs_root(explicit_docs_root: str | None) -> pathlib.Path | None:
    if explicit_docs_root:
        root = _normalize_docs_root(pathlib.Path(explicit_docs_root))
        return root if _is_valid_docs_root(root) else None

    for candidate in _candidate_roots():
        if _is_valid_docs_root(candidate):
            return candidate

    return None


def _shell_export(path: pathlib.Path) -> str:
    escaped = str(path).replace("'", "'\"'\"'")
    return f"export TREE_DATAGRID_DOCS_ROOT='{escaped}'"


def _run_command(cmd: list[str], cwd: pathlib.Path) -> None:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        details = stderr or stdout or f"exit code {completed.returncode}"
        raise RuntimeError(f"{' '.join(cmd)} failed: {details}")


def _build_api_docs(docs_root: pathlib.Path) -> None:
    _run_command(["dotnet", "tool", "restore"], cwd=docs_root)
    _run_command(
        ["dotnet", "tool", "run", "lunet", "--stacktrace", "build"],
        cwd=docs_root / "site",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Ensure TreeDataGrid Lunet docs are available locally. "
            "Validates repository-local site files and can build API artifacts on demand."
        )
    )
    parser.add_argument(
        "--docs-root",
        help="Path to repository root (or site directory) that should contain Lunet docs.",
    )
    parser.add_argument(
        "--api-json",
        help=(
            "Path to generated API JSON file. Defaults to the latest "
            "src/Avalonia.Controls.TreeDataGrid/obj/Release/*/"
            "Avalonia.Controls.TreeDataGrid.api.json under docs root."
        ),
    )
    parser.add_argument(
        "--build-api",
        action="store_true",
        help="Run Lunet build when API JSON file is missing.",
    )
    parser.add_argument(
        "--print-export",
        action="store_true",
        help="Print an export command for TREE_DATAGRID_DOCS_ROOT (for eval).",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    docs_root = _find_docs_root(args.docs_root)
    if docs_root is None:
        print("TreeDataGrid Lunet docs root not found.", file=sys.stderr)
        print(
            "Expected markers: " + ", ".join(REQUIRED_MARKERS),
            file=sys.stderr,
        )
        return 2

    api_json = _find_api_json(docs_root, args.api_json)

    if args.build_api and not api_json.exists():
        try:
            _build_api_docs(docs_root)
        except Exception as exc:  # pragma: no cover - process wrapper
            print(f"Failed to build Lunet API docs: {exc}", file=sys.stderr)
            return 2
        api_json = _find_api_json(docs_root, args.api_json)

    if args.build_api and not api_json.exists():
        print(
            "Lunet API JSON was not generated. "
            "Expected src/Avalonia.Controls.TreeDataGrid/obj/Release/*/Avalonia.Controls.TreeDataGrid.api.json.",
            file=sys.stderr,
        )
        return 2

    if args.print_export:
        print(_shell_export(docs_root))
    else:
        print(docs_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
