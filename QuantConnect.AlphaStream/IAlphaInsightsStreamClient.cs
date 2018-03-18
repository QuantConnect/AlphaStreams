﻿using System;
using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to receive streaming alpha insights.
    /// This client can subscribe and unsubscribe to individual alpha streams that have already been purchased.
    /// Please use the rest client to subscribe to a new alpha stream.
    /// </summary>
    public interface IAlphaInsightsStreamClient : IDisposable
    {
        /// <summary>
        /// Event fired for each insight received
        /// </summary>
        event EventHandler<InsightReceivedEventArgs> InsightReceived;

        /// <summary>
        /// Connect to the streaming insights server
        /// </summary>
        void Connect();

        /// <summary>
        /// Add an alpha insight stream to this client.
        /// The requested alpha stream must already be purchased.
        /// </summary>
        /// <param name="request">Request defining the alpha id of the stream to add</param>
        bool AddAlphaStream(AddInsightsStreamRequest request);

        /// <summary>
        /// Removes an alpha insight stream from this client
        /// </summary>
        /// <param name="request">Request defining which stream to remove</param>
        bool RemoveAlphaStream(RemoveInsightsStreamRequest request);
    }
}