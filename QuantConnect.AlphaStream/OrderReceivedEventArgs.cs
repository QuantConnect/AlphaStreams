using System;
using QuantConnect.AlphaStream.Models.Orders;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Event arguments fired when a new Order or Order update is received by the streaming client
    /// </summary>
    public class OrderReceivedEventArgs : EventArgs
    {
        /// <summary>
        /// Gets the alpha id that produced the heartbeat
        /// </summary>
        public string AlphaId { get; }

        /// <summary>
        /// The current order state
        /// </summary>
        public Order Order { get; }

        /// <summary>
        /// Creates a new instance
        /// </summary>
        public OrderReceivedEventArgs(string alphaId, Order order)
        {
            Order = order;
            AlphaId = alphaId;
        }
    }
}
