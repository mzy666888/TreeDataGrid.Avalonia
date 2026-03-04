using Avalonia.Automation.Peers;
using Avalonia.Controls;
using Xunit;

namespace Avalonia.Controls.TreeDataGridTests.Automation.Peers
{
    internal static class AutomationPeerTestHelper
    {
        public static TPeer CreatePeer<TPeer>(Control control)
            where TPeer : AutomationPeer
        {
            return Assert.IsType<TPeer>(ControlAutomationPeer.CreatePeerForElement(control));
        }
    }
}
