using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Subscribe to an Alpha given by id for a month and charge the subscription the funds account.
    /// </summary>
    [Endpoint(Method.POST, "alpha/{id}/subscribe")]
    public class SubscribeRequest : AttributeRequest<ApiResponse>
    {
        /// <summary>
        /// Identifier of the Alpha to subscribe.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }

        /// <summary>
        /// Try and subscribe to the Alpha with an exclusive preference.
        /// </summary>
        [QueryParameter("exclusive")]
        public bool Exclusive { get; set; }
    }
}