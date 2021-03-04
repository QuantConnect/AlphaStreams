using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch Alpha's latest bid
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}/prices/bids/read")]
    public class GetAlphaBidRequest : AttributeRequest<BidResult>
    {
        /// <summary>
        /// Unique id hash of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }
    }
}