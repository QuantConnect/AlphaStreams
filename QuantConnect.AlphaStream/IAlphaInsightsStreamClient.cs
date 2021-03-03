using QuantConnect.AlphaStream.Requests;

namespace QuantConnect.AlphaStream
{
    /// <summary>
    /// Client used to receive streaming alpha insights.
    /// This client can subscribe and unsubscribe to individual alpha streams that have already been purchased.
    /// </summary>
    /// <remarks>Kept for backwards compatibility <see cref="IAlphaStreamClient"/></remarks>
    public interface IAlphaInsightsStreamClient
    {
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