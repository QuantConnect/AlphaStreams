using QuantConnect.AlphaStream.Infrastructure;
using RestSharp;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Listing all alpha ids so you can maintain a dictionary and detect programatically when a new alpha is added to the API.
    /// </summary>
    [Endpoint(Method.GET, "alpha/list")]
    public class GetAlphaListRequest : AttributeRequest<List<string>>
    {
    }
}