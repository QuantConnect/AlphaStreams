using QuantConnect.AlphaStream.Infrastructure;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Streaming endpoint for insight predictions from the community. All subscribed Insights will be piped to this web socket connection 24/7.
    /// </summary>
    [Endpoint(Method.GET, "alpha/stream")]
    public class AlphaStreamRequest
    {
    }
}