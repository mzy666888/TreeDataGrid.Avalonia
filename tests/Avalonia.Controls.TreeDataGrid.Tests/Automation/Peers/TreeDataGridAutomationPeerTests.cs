using Avalonia.Automation.Peers;
using Avalonia.Controls;
using Avalonia.Controls.Automation.Peers;
using Avalonia.Headless.XUnit;
using Xunit;

namespace Avalonia.Controls.TreeDataGridTests.Automation.Peers
{
    public class TreeDataGridAutomationPeerTests
    {
        [AvaloniaFact]
        public void Should_Create_DataGrid_Peer()
        {
            var peer = AutomationPeerTestHelper.CreatePeer<TreeDataGridAutomationPeer>(new TreeDataGrid());

            Assert.Equal(AutomationControlType.DataGrid, peer.GetAutomationControlType());
            Assert.True(peer.IsControlElement());
            Assert.True(peer.IsContentElement());
        }
    }
}
