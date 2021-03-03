using System;
using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to receive streaming alpha insights, orders and order events.
    /// This client can subscribe and unsubscribe to individual alpha streams that have already been purchased.
    /// </summary>
    public interface IAlphaStreamClient : IDisposable
    {
        /// <summary>
        /// Event fired for each insight received
        /// </summary>
        event EventHandler<InsightReceivedEventArgs> InsightReceived;

        /// <summary>
        /// Event fired when a heartbeat is received
        /// </summary>
        event EventHandler<HeartbeatReceivedEventArgs> HeartbeatReceived;

        /// <summary>
        /// Event fired when a new Order or an update is received
        /// </summary>
        event EventHandler<OrderReceivedEventArgs> OrderReceived;

        /// <summary>
        /// Connect to the streaming insights server
        /// </summary>
        void Connect();

        /// <summary>
        /// Add an alpha stream to this client.
        /// The requested alpha stream must already be purchased.
        /// </summary>
        /// <param name="request">Request defining the alpha id of the stream to add</param>
        bool AddAlphaStream(AddAlphaStreamRequest request);

        /// <summary>
        /// Removes an alpha stream from this client
        /// </summary>
        /// <param name="request">Request defining which stream to remove</param>
        bool RemoveAlphaStream(RemoveAlphaStreamRequest request);
    }
}
