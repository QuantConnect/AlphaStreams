using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Read an individual information on an Alpha from the database based on the Alpha id.
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}")]
    public class GetAlphaByIdRequest : AttributeRequest<Alpha>
    {
        /// <summary>
        /// Unique id of an Alpha published to the marketplace.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }
    }
}