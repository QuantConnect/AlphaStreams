using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Create a bid price request.
    /// </summary>
    [Endpoint(Method.GET, "/alpha/{id}/prices/bids/create")]
    public class CreateBidPriceRequest : AttributeRequest<ApiResponse>
    {
        /// <summary>
        /// Unique id hash of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// Bid for the exclusive price (optional if shared is defined).
        /// </summary>
        [QueryParameter("exclusive")]
        public int ExclusivePrice { get; set; }

        /// <summary>
        /// Bid for the shared price (optional if exclusive is defined).
        /// </summary>
        [QueryParameter("shared")]
        public int SharedPrice { get; set; }

        /// <summary>
        /// Expiration time of the bid.
        /// </summary>
        [QueryParameter("good-until")]
        public long GoodUntil { get; set; }
    }
}