using System.Collections.Generic;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch the Alpha Insight list(backtest and live trading) track record since publication.
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}/insights")]
    public class GetAlphaInsightsRequest : AttributeRequest<List<AlphaStreamInsight>>
    {
        /// <summary>
        /// Unique id hash of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// Starting position for the search query. With very large datasets the results can be paginated and fetched in chunks starting from start.
        /// </summary>
        [QueryParameter("start")]
        public int Start { get; set; }
    }
}