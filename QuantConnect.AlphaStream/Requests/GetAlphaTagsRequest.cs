using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch number of alphas containing each tag
    /// </summary>
    [Endpoint(Method.GET, "alpha/tags/read")]
    public class GetAlphaTagsRequest : AttributeRequest<List<Tag>>
    {
    }
}
