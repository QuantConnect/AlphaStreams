using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Request used to remove an bid for an alpha
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}/prices/bids/delete")]
    public class RemoveAlphaBidRequest : AttributeRequest<ApiResponse>
    {
        /// <summary>
        /// Unique id hash of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// Unique id of an Bid made to the Alpha.
        /// </summary>
        [QueryParameter("bid-id")]
        public int BidId { get; set; }
    }
}