#!/usr/bin/env python3
"""Find API UIDs in Lunet-generated .api.json files."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
from dataclasses import dataclass

PREFERRED_API_JSON_RELATIVE = (
    "src/Avalonia.Controls.TreeDataGrid/obj/Release/net8.0/"
    "Avalonia.Controls.TreeDataGrid.api.json"
)


@dataclass(frozen=True)
class ApiEntry:
    uid: str
    name: str
    full_name: str
    kind: str
    source_file: pathlib.Path


def _default_api_json() -> pathlib.Path:
    def discover_for_root(root: pathlib.Path) -> pathlib.Path:
        preferred = root / PREFERRED_API_JSON_RELATIVE
        if preferred.exists():
            return preferred

        release_dir = root / "src" / "Avalonia.Controls.TreeDataGrid" / "obj" / "Release"
        candidates = list(release_dir.glob("*/Avalonia.Controls.TreeDataGrid.api.json"))
        candidates.sort(
            key=lambda path: (path.stat().st_mtime if path.exists() else 0, str(path)),
            reverse=True,
        )

        if candidates:
            return candidates[0]

        return preferred

    env_docs_root = os.environ.get("TREE_DATAGRID_DOCS_ROOT")
    if env_docs_root:
        env_path = pathlib.Path(env_docs_root).expanduser().resolve()
        candidate = discover_for_root(env_path)
        if candidate.exists():
            return candidate

    script_path = pathlib.Path(__file__).resolve()

    if len(script_path.parents) >= 4:
        repo_root = script_path.parents[3]
        repo_candidate = discover_for_root(repo_root)
        if repo_candidate.exists():
            return repo_candidate

    cwd = pathlib.Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        candidate = discover_for_root(parent)
        if candidate.exists():
            return candidate

    if len(script_path.parents) >= 4:
        return discover_for_root(script_path.parents[3])

    return discover_for_root(cwd)


def _resolve_api_json(api_json_arg: str | None) -> pathlib.Path:
    if api_json_arg:
        return pathlib.Path(api_json_arg).expanduser().resolve()
    return _default_api_json()


def _walk_entries(node: object, source_file: pathlib.Path, entries: list[ApiEntry]) -> None:
    if isinstance(node, dict):
        uid = node.get("uid")
        if isinstance(uid, str) and uid:
            name = node.get("name")
            full_name = node.get("fullName")
            kind = node.get("type")
            entries.append(
                ApiEntry(
                    uid=uid,
                    name=name if isinstance(name, str) else "",
                    full_name=full_name if isinstance(full_name, str) else "",
                    kind=kind if isinstance(kind, str) else "",
                    source_file=source_file,
                )
            )

        for value in node.values():
            _walk_entries(value, source_file, entries)
        return

    if isinstance(node, list):
        for item in node:
            _walk_entries(item, source_file, entries)


def _load_entries(api_json_path: pathlib.Path) -> list[ApiEntry]:
    with api_json_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    entries: list[ApiEntry] = []
    _walk_entries(payload, api_json_path, entries)
    return entries


def _score(entry: ApiEntry, query_cf: str) -> int:
    uid_cf = entry.uid.casefold()
    name_cf = entry.name.casefold()
    full_name_cf = entry.full_name.casefold()

    if uid_cf == query_cf:
        return 0
    if full_name_cf == query_cf or name_cf == query_cf:
        return 1
    if uid_cf.endswith(query_cf):
        return 2
    if query_cf in uid_cf:
        return 3
    if query_cf in full_name_cf:
        return 4
    if query_cf in name_cf:
        return 5
    return 999


def _to_display_path(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(pathlib.Path.cwd()))
    except ValueError:
        return str(path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find API UIDs in Lunet-generated .api.json files (exact or fuzzy)."
    )
    parser.add_argument("query", help="UID, type name, or substring to search for.")
    parser.add_argument(
        "--api-json",
        help="Path to the generated .api.json file.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of matches to print (default: 20).",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Match only exact UID values (case-insensitive).",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    api_json_path = _resolve_api_json(args.api_json)
    if not api_json_path.exists():
        print(f"API JSON file not found: {api_json_path}", file=sys.stderr)
        print(
            "Run `python3 skills/treedatagrid-for-avalonia-usage/scripts/ensure_lunet_docs.py --build-api` first.",
            file=sys.stderr,
        )
        return 2

    try:
        entries = _load_entries(api_json_path)
    except Exception as exc:
        print(f"Failed to read API JSON: {exc}", file=sys.stderr)
        return 2

    if not entries:
        print(f"No API entries found in: {api_json_path}", file=sys.stderr)
        return 2

    query_cf = args.query.casefold()
    if args.exact:
        matches = [entry for entry in entries if entry.uid.casefold() == query_cf]
    else:
        matches = [entry for entry in entries if _score(entry, query_cf) < 999]

    if not matches:
        print(
            f"No API matches found for '{args.query}' in {_to_display_path(api_json_path)}.",
            file=sys.stderr,
        )
        return 1

    best_by_uid: dict[str, ApiEntry] = {}
    for entry in matches:
        existing = best_by_uid.get(entry.uid)
        if existing is None:
            best_by_uid[entry.uid] = entry
            continue

        # Prefer entries with explicit type/name details.
        existing_score = (
            0 if existing.kind else 1,
            0 if existing.full_name else 1,
            0 if existing.name else 1,
        )
        current_score = (
            0 if entry.kind else 1,
            0 if entry.full_name else 1,
            0 if entry.name else 1,
        )
        if current_score < existing_score:
            best_by_uid[entry.uid] = entry

    deduped = sorted(
        best_by_uid.values(),
        key=lambda entry: (
            0 if args.exact else _score(entry, query_cf),
            len(entry.uid),
            entry.uid.casefold(),
        ),
    )

    limit = max(1, args.limit)
    shown = deduped[:limit]

    print(f"Query: {args.query}")
    print(f"API JSON: {_to_display_path(api_json_path)}")
    print(f"Matches: {len(deduped)} (showing {len(shown)})")
    print("")

    for index, entry in enumerate(shown, start=1):
        print(f"{index}. uid: {entry.uid}")
        if entry.kind:
            print(f"   type: {entry.kind}")
        if entry.name:
            print(f"   name: {entry.name}")
        if entry.full_name:
            print(f"   fullName: {entry.full_name}")
        print("")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
