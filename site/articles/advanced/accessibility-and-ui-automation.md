---
title: "Accessibility and UI Automation"
---

# Accessibility and UI Automation

TreeDataGrid exposes a full Avalonia automation surface for the grid root, rows, cells, and headers.

Use this layer when you need:

- screen-reader friendly selection and focus behavior
- reliable UI automation for tests or tooling
- custom control derivations that must preserve accessibility contracts

## Automation Peer Namespace

The public automation peer types live in [Namespace: Avalonia.Controls.Automation.Peers](../reference/namespace-automation-peers.md).

## Root Control Automation

[TreeDataGridAutomationPeer](xref:Avalonia.Controls.Automation.Peers.TreeDataGridAutomationPeer) represents the grid itself.

It exposes:

- `AutomationControlType.DataGrid`
- selection-provider behavior for row selection
- source-aware updates when the bound `ITreeDataGridSource` changes

## Row and Cell Automation

Realized rows and cells expose dedicated peers:

- [TreeDataGridRowAutomationPeer](xref:Avalonia.Controls.Automation.Peers.TreeDataGridRowAutomationPeer)
- [TreeDataGridCellAutomationPeer](xref:Avalonia.Controls.Automation.Peers.TreeDataGridCellAutomationPeer)
- [TreeDataGridCheckBoxCellAutomationPeer](xref:Avalonia.Controls.Automation.Peers.TreeDataGridCheckBoxCellAutomationPeer)

These peers bridge TreeDataGrid concepts to standard automation patterns:

- row selection
- expand/collapse for hierarchical rows
- toggle state for check box cells
- value-provider access where a row exposes textual value

## Header Automation

Column headers are surfaced separately:

- [TreeDataGridColumnHeaderAutomationPeer](xref:Avalonia.Controls.Automation.Peers.TreeDataGridColumnHeaderAutomationPeer)
- [TreeDataGridColumnHeadersPresenterAutomationPeer](xref:Avalonia.Controls.Automation.Peers.TreeDataGridColumnHeadersPresenterAutomationPeer)

This keeps header navigation and sortable-column discovery visible to automation clients without mixing that behavior into row peers.

## Guidance

- Prefer the built-in automation peers when using the standard control and templates.
- If you subclass TreeDataGrid or replace presenter elements, keep the same automation roles and provider contracts.
- Test accessibility-sensitive changes together with selection, expansion, and check box interaction.

## API Coverage Checklist

- <xref:Avalonia.Controls.Automation.Peers.TreeDataGridAutomationPeer>
- <xref:Avalonia.Controls.Automation.Peers.TreeDataGridRowAutomationPeer>
- <xref:Avalonia.Controls.Automation.Peers.TreeDataGridCellAutomationPeer>
- <xref:Avalonia.Controls.Automation.Peers.TreeDataGridCheckBoxCellAutomationPeer>
- <xref:Avalonia.Controls.Automation.Peers.TreeDataGridColumnHeaderAutomationPeer>
- <xref:Avalonia.Controls.Automation.Peers.TreeDataGridColumnHeadersPresenterAutomationPeer>

## Related

- [Namespace: Avalonia.Controls.Automation.Peers](../reference/namespace-automation-peers.md)
- [Guides: Events and User Interaction](../guides/events-and-user-interaction.md)
- [Advanced: Diagnostics and Testing](diagnostics-and-testing.md)
