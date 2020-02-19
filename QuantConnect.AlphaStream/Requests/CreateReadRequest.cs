using QuantConnect.AlphaStream.Infrastructure;
using QuantConnect.AlphaStream.Models;
using RestSharp;
using System.Collections.Generic;

namespace QuantConnect.AlphaStream.Requests
{
    /// <summary>
    /// Read a conversation thread.
    /// Read a conversation with the author(s) of the alpha via email. Quickly solve reconciliation issues or design automated filter questions.
    /// </summary>
    [Endpoint(Method.GET, "alpha/{id}/conversations/read")]
    public class CreateReadRequest : AttributeRequest<List<Conversation>>
    {
        ///<summary>
        /// Unique id hash of an Alpha published to the marketplace
        /// </summary>
        [PathParameter("id")]
        public string Id { get; set; }
    }
}
