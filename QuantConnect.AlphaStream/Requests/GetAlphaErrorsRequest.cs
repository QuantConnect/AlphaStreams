using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch Alpha runtime errors to help correlate unknown behavior or protect against exposure when an Alpha has a production issue.
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}/errors")]
    public class GetAlphaErrorsRequest : AttributeRequest<List<RuntimeError>>
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
        public int Start { get; set; } = 0;
    }
}