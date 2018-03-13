using System.Collections.Generic;
using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch the insight backtest results and the live insight track record since publication.
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}/insights")]
    public class GetAlphaInsightsRequest : AttributeRequest<List<Insight>>
    {
        /// <summary>
        /// Unique id of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// The start index of the search. This is used to support pagination
        /// </summary>
        [QueryParameter("start")]
        public int Start { get; set; }
    }
}