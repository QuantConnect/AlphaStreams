using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Unsubscribe to the Alpha given by the id in path. Pro-rate subscription billing for remainder of them billing cycle.
    /// </summary>
    [Endpoint(Method.POST, "alpha/{id}/unsubscribe")]
    public class UnsubscribeRequest : AttributeRequest<ApiResponse>
    {
        /// <summary>
        /// Identifier of the Alpha to unsubscribe
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }
    }
}