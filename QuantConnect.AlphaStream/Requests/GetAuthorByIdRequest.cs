using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Fetch Author information by id to form models based around people.
    /// </summary>
    [Endpoint(Method.GET, "alpha/author/{id}")]
    public class GetAuthorByIdRequest : AttributeRequest<Author>
    {
        /// <summary>
        /// Unique id hash of an Author.
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }
    }
}