# TreeDataGrid Lunet Navigation

## Table of Contents
- [Preflight](#preflight)
- [Primary Entry Points](#primary-entry-points)
- [Task Routing Matrix](#task-routing-matrix)
- [Namespace Reference Pages](#namespace-reference-pages)
- [API UID Lookup Workflow](#api-uid-lookup-workflow)
- [Fast Search Commands](#fast-search-commands)

## Preflight

Before opening docs, ensure they are available and export the docs root:

```bash
eval "$(python3 skills/treedatagrid-for-avalonia-usage/scripts/ensure_lunet_docs.py --print-export)"
```

If the skill is installed in `$CODEX_HOME`:

```bash
eval "$(python3 "${CODEX_HOME:-$HOME/.codex}/skills/treedatagrid-for-avalonia-usage/scripts/ensure_lunet_docs.py" --print-export)"
```

All `site/...` and `src/...` paths in this file are relative to `$TREE_DATAGRID_DOCS_ROOT`.

## Primary Entry Points

- `site/readme.md`
- `site/articles/readme.md`
- `site/articles/reference/api-coverage-index.md`
- `src/Avalonia.Controls.TreeDataGrid/obj/Release/*/Avalonia.Controls.TreeDataGrid.api.json`

Start from these files before opening lower-level pages.

## Task Routing Matrix

Use this matrix to choose article sources before coding.

| User task | Start with these articles | Add these supporting UIDs |
|---|---|---|
| Install and first setup | `site/articles/getting-started/installation.md`, `site/articles/getting-started/overview.md` | `Avalonia.Controls.TreeDataGrid` |
| Flat source configuration | `site/articles/getting-started/quickstart-flat.md`, `site/articles/guides/sources-flat.md` | ``Avalonia.Controls.FlatTreeDataGridSource`1``, ``Avalonia.Controls.ITreeDataGridSource`1`` |
| Hierarchical source configuration | `site/articles/getting-started/quickstart-hierarchical.md`, `site/articles/guides/sources-hierarchical.md` | ``Avalonia.Controls.HierarchicalTreeDataGridSource`1``, ``Avalonia.Controls.Models.TreeDataGrid.HierarchicalExpanderColumn`1`` |
| Text columns | `site/articles/guides/column-text.md`, `site/articles/concepts/columns-cells-rows.md` | ``Avalonia.Controls.Models.TreeDataGrid.TextColumn`2``, ``Avalonia.Controls.Models.TreeDataGrid.TextColumnOptions`1`` |
| CheckBox columns | `site/articles/guides/column-checkbox.md`, `site/articles/concepts/columns-cells-rows.md` | ``Avalonia.Controls.Models.TreeDataGrid.CheckBoxColumn`1``, ``Avalonia.Controls.Models.TreeDataGrid.CheckBoxColumnOptions`1`` |
| Template columns | `site/articles/guides/column-template.md`, `site/articles/guides/templates-and-styling.md` | ``Avalonia.Controls.Models.TreeDataGrid.TemplateColumn`1``, ``Avalonia.Controls.Models.TreeDataGrid.TemplateColumnOptions`1`` |
| Expander/hierarchy columns | `site/articles/guides/column-expander.md`, `site/articles/guides/expansion-and-programmatic-navigation.md` | ``Avalonia.Controls.Models.TreeDataGrid.HierarchicalExpanderColumn`1``, ``Avalonia.Controls.Models.TreeDataGrid.IExpanderColumn`1`` |
| Sorting and widths | `site/articles/guides/sorting-and-column-widths.md` | ``Avalonia.Controls.Models.TreeDataGrid.ColumnOptions`1``, ``Avalonia.Controls.Models.TreeDataGrid.SortableRowsBase`2`` |
| Editing gestures | `site/articles/guides/editing-and-begin-edit-gestures.md` | `Avalonia.Controls.Models.TreeDataGrid.BeginEditGestures`, `Avalonia.Controls.Models.TreeDataGrid.ICellOptions` |
| Row selection | `site/articles/guides/selection-row.md`, `site/articles/concepts/selection-models.md` | ``Avalonia.Controls.Selection.TreeDataGridRowSelectionModel`1``, ``Avalonia.Controls.Selection.ITreeDataGridRowSelectionModel`1`` |
| Cell selection | `site/articles/guides/selection-cell.md`, `site/articles/concepts/selection-models.md` | ``Avalonia.Controls.Selection.TreeDataGridCellSelectionModel`1``, ``Avalonia.Controls.Selection.ITreeDataGridCellSelectionModel`1`` |
| Selection internals and batching | `site/articles/advanced/selection-internals-and-batch-update.md` | ``Avalonia.Controls.Selection.TreeSelectionModelBase`1``, ``Avalonia.Controls.Selection.TreeSelectionModelBase`1.BatchUpdateOperation`` |
| Programmatic expansion | `site/articles/guides/expansion-and-programmatic-navigation.md` | ``Avalonia.Controls.Models.TreeDataGrid.HierarchicalRows`1``, `Avalonia.Controls.Models.TreeDataGrid.IExpander` |
| Drag and drop rows | `site/articles/guides/drag-and-drop-rows.md` | `Avalonia.Controls.TreeDataGridRowDragEventArgs`, `Avalonia.Controls.TreeDataGridRowDropPosition` |
| TreeDataGrid events | `site/articles/guides/events-and-user-interaction.md` | `Avalonia.Controls.TreeDataGrid`, `Avalonia.Controls.TreeDataGridCellEventArgs` |
| ItemsSourceView integration | `site/articles/guides/working-with-itemssourceview.md` | ``Avalonia.Controls.TreeDataGridItemsSourceView`1``, `Avalonia.Controls.TreeDataGridItemsSourceView` |
| Templates and styling | `site/articles/guides/templates-and-styling.md` | `Avalonia.Controls.Converters.IndentConverter`, `Avalonia.Controls.Primitives.TreeDataGridTemplateCell` |
| XAML usage patterns | `site/articles/xaml/overview.md`, `site/articles/xaml/samples-walkthrough.md` | `Avalonia.Controls.TreeDataGrid` |
| Theme usage and customization | `site/articles/xaml/theme-usage.md`, `site/articles/xaml/theme-customization.md`, `site/articles/xaml/theme-resource-keys-reference.md` | `Avalonia.Controls.Primitives.TreeDataGridCell`, `Avalonia.Controls.Primitives.TreeDataGridColumnHeader` |
| ControlTheme overrides/replacement | `site/articles/xaml/control-theme-overrides-basedon.md`, `site/articles/xaml/control-theme-full-replacement.md` | `Avalonia.Controls.Primitives.TreeDataGridRowsPresenter`, `Avalonia.Controls.Primitives.TreeDataGridCellsPresenter` |
| Performance and virtualization | `site/articles/advanced/performance-virtualization-and-realization.md` | `Avalonia.Controls.Primitives.TreeDataGridRowsPresenter`, `Avalonia.Controls.Primitives.TreeDataGridColumnHeadersPresenter` |
| Primitive control internals | `site/articles/advanced/primitives-overview.md` | `Avalonia.Controls.Primitives.TreeDataGridElementFactory` |
| Custom element factory | `site/articles/advanced/custom-element-factory.md` | `Avalonia.Controls.Primitives.TreeDataGridElementFactory` |
| Custom rows/columns pipeline | `site/articles/advanced/custom-rows-columns-pipeline.md` | ``Avalonia.Controls.Models.TreeDataGrid.SortableRowsBase`2``, ``Avalonia.Controls.Models.TreeDataGrid.AnonymousSortableRows`1`` |
| Typed binding internals | `site/articles/advanced/typed-binding.md` | ``Avalonia.Experimental.Data.TypedBinding`1``, ``Avalonia.Experimental.Data.Core.TypedBindingExpression`2`` |
| Diagnostics/testing strategy | `site/articles/advanced/diagnostics-and-testing.md`, `site/articles/guides/troubleshooting.md` | `Avalonia.Controls.TreeDataGrid`, `Avalonia.Controls.ITreeDataGridSource` |

## Namespace Reference Pages

Load namespace reference pages when the task spans many related symbols:

- `site/articles/reference/namespace-avalonia-controls.md`
- `site/articles/reference/namespace-models-treedatagrid.md`
- `site/articles/reference/namespace-selection.md`
- `site/articles/reference/namespace-primitives.md`
- `site/articles/reference/namespace-experimental.md`
- `site/articles/reference/namespace-converters-and-models.md`

Use `site/articles/reference/api-coverage-index.md` to map any public type to a primary article.

## API UID Lookup Workflow

1. Run the UID finder script:

   ```bash
   python3 skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py <query>
   ```

   If the skill is installed in `$CODEX_HOME`:

   ```bash
   python3 "${CODEX_HOME:-$HOME/.codex}/skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py" <query>
   ```

   For generic UIDs containing backticks, quote the value:

   ```bash
   python3 "${CODEX_HOME:-$HOME/.codex}/skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py" 'Avalonia.Controls.Models.TreeDataGrid.TextColumn`2' --exact
   ```

2. Confirm `uid`, `name`, `fullName`, and `type` in script output.
3. Open generated HTML page under `site/.lunet/build/www/api/` when visual inspection is needed.
4. Cross-link to the narrative article from `api-coverage-index.md`.

## Fast Search Commands

Use these when you need ad-hoc discovery:

```bash
rg -n "TreeDataGrid|FlatTreeDataGridSource|HierarchicalTreeDataGridSource" "$TREE_DATAGRID_DOCS_ROOT/site/articles"
rg -n "^# " "$TREE_DATAGRID_DOCS_ROOT/site/articles/guides" "$TREE_DATAGRID_DOCS_ROOT/site/articles/advanced" "$TREE_DATAGRID_DOCS_ROOT/site/articles/xaml"
python3 "$TREE_DATAGRID_DOCS_ROOT/skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py" TreeDataGrid
python3 "$TREE_DATAGRID_DOCS_ROOT/skills/treedatagrid-for-avalonia-usage/scripts/find_lunet_api.py" 'TreeSelectionModelBase`1'
```
