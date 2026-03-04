---
name: treedatagrid-for-avalonia-usage
description: Implement, troubleshoot, and review TreeDataGrid usage in this repository by grounding work in Lunet articles (`site/articles/**`) and generated API data (`src/Avalonia.Controls.TreeDataGrid/obj/Release/*/Avalonia.Controls.TreeDataGrid.api.json`). Use when tasks involve TreeDataGrid setup, flat or hierarchical sources, columns/cells/rows, selection, editing, drag and drop, XAML themes/templates, performance/primitives internals, or public API lookup.
---

# TreeDataGrid for Avalonia Usage

## Quick Start

- Run preflight and export docs root (repo-local skill path):

```bash
eval "$(python3 skills/treedatagrid-for-avalonia-usage/scripts/ensure_lunet_docs.py --print-export)"
```

- If the skill is installed in `$CODEX_HOME`, run:

```bash
eval "$(python3 "${CODEX_HOME:-$HOME/.codex}/skills/treedatagrid-for-avalonia-usage/scripts/ensure_lunet_docs.py" --print-export)"
```

- Route the request with [`references/lunet-navigation.md`](references/lunet-navigation.md).
- Read narrative guidance from `$TREE_DATAGRID_DOCS_ROOT/site/articles/**` before editing code.
- Resolve member-level behavior from generated API data before finalizing implementation details.
- Include exact article paths and API UIDs in the final response.

## Workflow

### 0. Ensure Lunet docs are available

- Run `scripts/ensure_lunet_docs.py` before opening docs.
- Preflight behavior:
- Reuse local docs when `site/config.scriban` and `site/articles/readme.md` already exist.
- This preflight does not fetch from network; it validates repository-local docs only.
- Use `--build-api` to run Lunet build if API artifacts are missing.
- Export `TREE_DATAGRID_DOCS_ROOT` for all subsequent article/API lookups.

### 1. Route Request to the Right Article Set

- Map the user request to one or more article groups:
- `getting-started/` for onboarding and first implementation.
- `guides/` for feature work (sources, columns, selection, editing, drag and drop, styling).
- `xaml/` for `ControlTheme`, template keys, and resource customization.
- `advanced/` for internals, performance, element factories, and typed binding.
- `reference/` for type-to-article mapping and namespace entry pages.

### 2. Read Canonical Narrative Docs First

- Open the primary article for the task.
- Open the related conceptual page when the task touches indices, rows, columns, or selection semantics.
- Open the matching namespace reference page from `site/articles/reference/`.

### 3. Confirm API Contracts from Lunet API Data

- Start with `site/articles/reference/api-coverage-index.md` to map a type to its primary article.
- Query generated API data with the UID finder script.
- Run (repo-local skill path):

```bash
python3 skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py <uid-or-fragment>
```

- If the skill is installed in `$CODEX_HOME`, run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py" <uid-or-fragment>
```

- Use `--exact` when the UID is known and deterministic lookup is required.
- For generic UIDs that contain backticks, quote the argument:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py" 'Avalonia.Controls.Models.TreeDataGrid.TextColumn`2' --exact
```

### 4. Implement and Verify

- Align code changes with the documented behavior from articles and API data.
- Validate with targeted tests for behavior changes.
- Build docs if article references or links are edited.
- If docs and source diverge, inspect source code and call out the mismatch explicitly.

### 5. Report Evidence

- Report the exact files used as evidence:
- article paths from `site/articles/**`
- API UIDs from generated API data
- commands/tests executed and outcomes

## High-Value Entry Points

- Paths below are relative to `$TREE_DATAGRID_DOCS_ROOT`.
- `site/readme.md`
- `site/articles/readme.md`
- `site/articles/reference/api-coverage-index.md`
- `site/articles/reference/namespace-avalonia-controls.md`
- `site/articles/reference/namespace-models-treedatagrid.md`
- `site/articles/reference/namespace-selection.md`
- `site/articles/reference/namespace-primitives.md`
- `src/Avalonia.Controls.TreeDataGrid/obj/Release/*/Avalonia.Controls.TreeDataGrid.api.json`
- `references/lunet-navigation.md`

## Resources

### scripts/

- `scripts/ensure_lunet_docs.py`: Validate repository-local Lunet docs and optionally build API artifacts.
- `scripts/find_lunet_api.py`: Query generated API JSON for exact and fuzzy UID matches.

### references/

- `references/lunet-navigation.md`: Route user tasks to canonical Lunet article and API entry points quickly.
